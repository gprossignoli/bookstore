from datetime import datetime

from bookstore.application.event_bus.event_unique_identifier_to_mapper import (
    EventUniqueIdentifierToMapper,
)
from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)


class OutboxRecordToEventTranslator:
    def __init__(self):
        self.__event_unique_identifier_to_mapper = EventUniqueIdentifierToMapper()

    def translate(self, record: OutboxRecord) -> Event:
        event_klass = self.__event_unique_identifier_to_mapper.get_event(
            record.event_unique_identifier
        )
        created_at = datetime.strftime(record.created_at, Event.DATE_TIME_FORMAT)
        return event_klass.reconstruct(
            event_id=record.id, created_at=created_at, payload=record.payload
        )
