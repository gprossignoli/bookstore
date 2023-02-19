from bookstore.models.book import Book


class BookNotFoundException(Exception):
	pass


class BookRepository:
	def get_or_fail(self, book_id: int) -> Book:
		book = Book.query.filter_by(id=book_id).first()
		if book is None:
			raise BookNotFoundException()

		return book
