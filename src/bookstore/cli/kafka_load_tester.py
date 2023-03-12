import random

from bookstore.application import CommandExecutor
from bookstore.application.purchase_book import PurchaseBookCommand
from bookstore.infrastructure.repositories import UserRepository, BookRepository
from bookstore.models.book_exception import BookException
from bookstore.settings import logger


class KafkaLoadTester:
	def __init__(self):
		self.__user_repository = UserRepository()
		self.__book_repository = BookRepository()

	def __load_users(self):
		return self.__user_repository.get_user_ids(max_users=10)

	def __load_books(self):
		return self.__book_repository.get_books_ids(max_books=10)

	def execute(self):
		users = self.__load_users()
		books = self.__load_books()

		for book in books:
			try:
				purchase_book_command = PurchaseBookCommand(book_id=book, user_id=random.choice(users),
															quantity=random.randint(1, 5))

				CommandExecutor().execute(purchase_book_command)
				logger.info(f"Use case completed for {book}")
			except BookException as e:
				logger.error(f"Use case completed for {book}, error: {e}")

