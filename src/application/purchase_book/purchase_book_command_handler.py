from flask_sqlalchemy.session import Session

from models.purchase import Purchase
from models.purchase_exception import PurchaseException
from repositories.book_repository import BookRepository, BookNotFoundException
from repositories.user_repository import UserRepository
from settings import db
from src.application.command_handler import CommandHandler
from src.application.purchase_book.purchase_book_command import PurchaseBookCommand


"""
generar un modelo purchase con los datos del command, añadiendo created_at
guardar en db el purchase
crear el evento purchase_created
publicar el evento
"""


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

		purchase = Purchase(book_id=command.book_id, user_id=command.user_id, quantity=command.quantity)
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
