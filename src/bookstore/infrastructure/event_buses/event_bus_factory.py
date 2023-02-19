from abc import ABC, abstractmethod

from bookstore.infrastructure.event_buses import EventBus


class EventBusFactory(ABC):
	@abstractmethod
	def build(self) -> EventBus:
		pass
