from abc import ABC, abstractmethod

from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)


class TransactionalOutboxRepository(ABC):
    @abstractmethod
    def save(self, record: OutboxRecord) -> None:
        pass
