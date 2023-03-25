from bookstore.application.command_handler import CommandHandler
from bookstore.application.purchase_book.purchase_book_command import (
    PurchaseBookCommand,
)
from bookstore.application.repositories import BookRepository, UserRepository
from bookstore.domain.book_not_found_exception import BookNotFoundException
from bookstore.domain.user_not_found_exception import UserNotFoundException
from bookstore.application.event_bus import EventBusProducer
from bookstore.domain.purchase_book import PurchaseCreatedEvent
from bookstore.models.purchase import Purchase
from bookstore.models.purchase_exception import PurchaseException
from bookstore.settings import db


class PurchaseBookCommandHandler(CommandHandler):
    def __init__(self, book_repository: BookRepository, user_repository: UserRepository, event_bus: EventBusProducer):
        self.__book_repository = book_repository
        self.__user_repository = user_repository
        self.__event_bus = event_bus

    def execute(self, command: PurchaseBookCommand) -> None:
        try:
            book = self.__book_repository.get_or_fail(book_id=command.book_id)
        except BookNotFoundException:
            raise PurchaseException("Book not exists")

        try:
            self.__user_repository.get_or_fail(user_id=command.user_id)
        except UserNotFoundException:
            raise PurchaseException("User not exists")

        if book.stock == 0 or book.stock - command.quantity < 0:
            raise PurchaseException(f"No stock available for the book {book.id}")

        purchase = Purchase(
            book_id=command.book_id,
            user_id=command.user_id,
            quantity=command.quantity,
            price=book.price,
        )
        book.stock -= command.quantity

        session = db.session
        try:
            session.add(book)
            session.add(purchase)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

        purchase_event = PurchaseCreatedEvent(
            book_id=book.id,
            quantity=purchase.quantity,
            user_id=purchase.user_id,
            price=purchase.price,
        )
        self.__event_bus.publish(purchase_event)
