from abc import abstractmethod, ABC
from typing import Iterable

from bookstore.models.book import Book


class BookRepository(ABC):
	@abstractmethod
	def get_or_fail(self, book_id: int) -> Book:
		pass

	@abstractmethod
	def get_books_ids(self, max_books: int) -> Iterable[int]:
		pass
