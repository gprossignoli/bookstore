from flask_sqlalchemy.session import Session

from src.models.purchase import Purchase
from src.models.purchase_exception import PurchaseException
from src.infrastructure.repositories import BookRepository, BookNotFoundException
from src.infrastructure.repositories import UserRepository
from settings import db
from src.application.command_handler import CommandHandler
from src.application.purchase_book.purchase_book_command import PurchaseBookCommand


class PurchaseBookCommandHandler(CommandHandler):
	def __init__(self):
		self.book_repository = BookRepository()
		self.user_repository = UserRepository()

	def execute(self, command: PurchaseBookCommand) -> None:
		try:
			book = self.book_repository.get_or_fail(book_id=command.book_id)
		except BookNotFoundException:
			raise PurchaseException("Book not exists")

		try:
			self.user_repository.get_or_fail(user_id=command.user_id)
		except BookNotFoundException:
			raise PurchaseException("User not exists")

		if book.stock == 0 or book.stock - command.quantity < 0:
			raise PurchaseException(f"No stock available for the book {book.id}")

		purchase = Purchase(book_id=command.book_id, user_id=command.user_id, quantity=command.quantity, price=book.price)
		book.stock -= command.quantity

		session = Session(db)
		try:
			session.add(book)
			session.add(purchase)
			session.commit()
		except Exception as e:
			session.rollback()
			raise e

		# Publicar evento aqui
