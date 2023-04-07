from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses.debezium_outbox.debezium_record import DebeziumRecord


class EventToDebeziumRecordTranslator:
    def translate(self, event: Event) -> DebeziumRecord:
        return DebeziumRecord(
            event_id=event.id,
            event_unique_identifier=event.unique_identifier(),
            payload=event.body,
            created_at=event.created_at,
        )
