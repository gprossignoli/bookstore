import json

from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)


class EventToOutboxRecordTranslator:
    def translate(self, event: Event) -> OutboxRecord:
        return OutboxRecord(
            event_id=event.id,
            event_unique_identifier=event.unique_identifier(),
            payload=event.body,
            created_at=event.created_at,
            delivered_at=None,
            delivery_errors=0,
            delivery_paused_at=None,
        )
