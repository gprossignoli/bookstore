from dataclasses import dataclass

from bookstore.application.command import Command


@dataclass()
class PurchaseBookCommand(Command):
    book_id: int
    user_id: str
    quantity: int

    @classmethod
    def fqn(cls) -> str:
        return "command.purchase_book"
