from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)
from bookstore.infrastructure.event_buses.transactional_outbox.transactional_outbox_repository import (
    TransactionalOutboxRepository,
)
from bookstore.settings import db


class SqlalchemyTransactionalOutboxRepository(TransactionalOutboxRepository):
    def save(self, record: OutboxRecord) -> None:
        db.session.add(record)
