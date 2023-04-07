from abc import ABC, abstractmethod
from typing import Iterable

from bookstore.infrastructure.event_buses.debezium_outbox.debezium_record import DebeziumRecord


class DebeziumOutboxRepository(ABC):
    @abstractmethod
    def save(self, record: DebeziumRecord) -> None:
        pass

    @abstractmethod
    def find(self, batch_size: int = 100) -> Iterable[DebeziumRecord]:
        pass
