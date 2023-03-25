from bookstore.application.event_bus import EventBusProducer
from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses.transactional_outbox.event_to_outbox_record_translator import (
    EventToOutboxRecordTranslator,
)
from bookstore.infrastructure.event_buses.transactional_outbox.transactional_outbox_repository import (
    TransactionalOutboxRepository,
)


class TransactionalOutboxEventBusProducer(EventBusProducer):
    def __init__(
        self,
        event_to_outbox_record_translator: EventToOutboxRecordTranslator,
        outbox_repository: TransactionalOutboxRepository,
    ):
        self.__event_to_outbox_record_translator = event_to_outbox_record_translator
        self.__outbox_repository = outbox_repository

    def publish(self, event: Event) -> None:
        outbox_record = self.__event_to_outbox_record_translator.translate(event)
        self.__outbox_repository.save(outbox_record)
