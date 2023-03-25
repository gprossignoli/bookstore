from bookstore.application.command import Command
from bookstore.application.purchase_book.purchase_book_command import (
    PurchaseBookCommand,
)
from bookstore.application.purchase_book.purchase_book_command_handler import (
    PurchaseBookCommandHandler,
)
from bookstore.infrastructure.event_buses import KafkaEventBusProducerFactory
from bookstore.infrastructure.repositories import SqlalchemyBookRepository, SqlalchemyUserRepository


class CommandExecutor:
    def __init__(self):
        self.__mapper = {
            PurchaseBookCommand.fqn(): PurchaseBookCommandHandler(
                book_repository=SqlalchemyBookRepository(),
                user_repository=SqlalchemyUserRepository(),
                event_bus=KafkaEventBusProducerFactory().build()
            )
        }

    def execute(self, command: Command) -> None:
        self.__mapper.get(command.fqn()).execute(command=command)
