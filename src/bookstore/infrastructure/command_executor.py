from bookstore.application.command import Command
from bookstore.application.purchase_book.purchase_book_command import (
    PurchaseBookCommand,
)
from bookstore.application.purchase_book.purchase_book_command_handler import (
    PurchaseBookCommandHandler,
)
from bookstore.infrastructure.event_buses.debezium_outbox.debezium_outbox_event_bus_producer import (
    DebeziumOutboxEventBusProducer,
)
from bookstore.infrastructure.event_buses.debezium_outbox.event_to_debezium_record_translator import (
    EventToDebeziumRecordTranslator,
)
from bookstore.infrastructure.event_buses.debezium_outbox.sqlalchemy_debezium_outbox_repository import (
    SqlalchemyDebeziumOutboxRepository,
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
                event_bus=DebeziumOutboxEventBusProducer(
                    event_to_debezium_record_translator=EventToDebeziumRecordTranslator(),
                    debezium_outbox_repository=SqlalchemyDebeziumOutboxRepository(),
                ),
            )
        }

    def execute(self, command: Command) -> None:
        self.__mapper.get(command.fqn()).execute(command=command)
