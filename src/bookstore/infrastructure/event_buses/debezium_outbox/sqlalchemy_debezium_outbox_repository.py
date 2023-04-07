from typing import Iterable

from bookstore.infrastructure.event_buses.debezium_outbox.debezium_outbox_repository import DebeziumOutboxRepository
from bookstore.infrastructure.event_buses.debezium_outbox.debezium_record import DebeziumRecord
from bookstore.settings import db


class SqlalchemyDebeziumOutboxRepository(DebeziumOutboxRepository):
    def save(self, record: DebeziumRecord) -> None:
        db.session.add(record)

    def find(self, **kwargs) -> Iterable[DebeziumRecord]:
        return NotImplemented
