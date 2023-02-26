from flask_sqlalchemy.session import Session

from bookstore.settings import db
from bookstore.domain.purchase_book import PurchaseCreatedEvent
from bookstore.models.purchase import Purchase
from bookstore.models.purchase_exception import PurchaseException
from bookstore.application.command_handler import CommandHandler
from bookstore.application.purchase_book.purchase_book_command import PurchaseBookCommand
from bookstore.infrastructure.event_buses import EventBus
from bookstore.infrastructure.repositories import BookRepository, BookNotFoundException
from bookstore.infrastructure.repositories import UserRepository


class PurchaseBookCommandHandler(CommandHandler):
	def __init__(self, event_bus: EventBus):
		self.__book_repository = BookRepository()
		self.__user_repository = UserRepository()
		self.__event_bus = event_bus

	def execute(self, command: PurchaseBookCommand) -> None:
		try:
			book = self.__book_repository.get_or_fail(book_id=command.book_id)
		except BookNotFoundException:
			raise PurchaseException("Book not exists")

		try:
			self.__user_repository.get_or_fail(user_id=command.user_id)
		except BookNotFoundException:
			raise PurchaseException("User not exists")

		if book.stock == 0 or book.stock - command.quantity < 0:
			raise PurchaseException(f"No stock available for the book {book.id}")

		purchase = Purchase(book_id=command.book_id, user_id=command.user_id, quantity=command.quantity, price=book.price)
		book.stock -= command.quantity

		session = db.session
		try:
			session.add(book)
			session.add(purchase)
			session.commit()
		except Exception as e:
			session.rollback()
			raise e

		# Publicar evento aqui
		purchase_event = PurchaseCreatedEvent(book_id=book.id, quantity=purchase.quantity,
											  user_id=purchase.user_id, price=purchase.price)
		self.__event_bus.publish(purchase_event)
