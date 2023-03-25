from typing import List

from bookstore.application.repositories import BookRepository
from bookstore.domain.book_not_found_exception import BookNotFoundException
from bookstore.models.book import Book


class SqlalchemyBookRepository(BookRepository):
    def get_or_fail(self, book_id: int) -> Book:
        book = Book.query.filter_by(id=book_id).first()
        if book is None:
            raise BookNotFoundException()

        return book

    def get_books_ids(self, max_books: int) -> List[int]:
        books = Book.query.filter(Book.stock > 0).limit(max_books).all()

        return [book.id for book in books]
