from bookstore.application.command import Command
from bookstore.application.purchase_book.purchase_book_command import (
    PurchaseBookCommand,
)
from bookstore.application.purchase_book.purchase_book_command_handler import (
    PurchaseBookCommandHandler,
)
from bookstore.infrastructure.event_buses.transactional_outbox.event_to_outbox_record_translator import (
    EventToOutboxRecordTranslator,
)
from bookstore.infrastructure.event_buses.transactional_outbox.sqlalchemy_transactional_outbox_repository import (
    SqlalchemyTransactionalOutboxRepository,
)
from bookstore.infrastructure.event_buses.transactional_outbox.transactional_outbox_event_bus_producer import (
    TransactionalOutboxEventBusProducer,
)
from bookstore.infrastructure.repositories import (
    SqlalchemyBookRepository,
    SqlalchemyUserRepository,
)


class CommandExecutor:
    def __init__(self):
        self.__mapper = {
            PurchaseBookCommand.fqn(): PurchaseBookCommandHandler(
                book_repository=SqlalchemyBookRepository(),
                user_repository=SqlalchemyUserRepository(),
                event_bus=TransactionalOutboxEventBusProducer(
                    event_to_outbox_record_translator=EventToOutboxRecordTranslator(),
                    outbox_repository=SqlalchemyTransactionalOutboxRepository(),
                ),
            )
        }

    def execute(self, command: Command) -> None:
        self.__mapper.get(command.fqn()).execute(command=command)
