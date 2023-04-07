from bookstore.application.event_bus import EventBusProducer
from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses.debezium_outbox.debezium_outbox_repository import DebeziumOutboxRepository
from bookstore.infrastructure.event_buses.debezium_outbox.event_to_debezium_record_translator import \
    EventToDebeziumRecordTranslator


class DebeziumOutboxEventBusProducer(EventBusProducer):
    def __init__(
        self,
        event_to_debezium_record_translator: EventToDebeziumRecordTranslator,
        debezium_outbox_repository: DebeziumOutboxRepository,
    ):
        self.__event_to_debezium_record_translator = event_to_debezium_record_translator
        self.__debezium_outbox_repository = debezium_outbox_repository

    def publish(self, event: Event) -> None:
        outbox_record = self.__event_to_debezium_record_translator.translate(event)
        self.__debezium_outbox_repository.save(outbox_record)
