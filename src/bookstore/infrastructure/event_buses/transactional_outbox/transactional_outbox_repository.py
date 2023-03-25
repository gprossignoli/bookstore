from abc import ABC, abstractmethod
from typing import Iterable

from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)


class TransactionalOutboxRepository(ABC):
    @abstractmethod
    def save(self, record: OutboxRecord) -> None:
        pass

    @abstractmethod
    def find(self, batch_size: int = 100) -> Iterable[OutboxRecord]:
        pass
