from abc import ABC, abstractmethod

from infrastructure.event_buses.event_bus import EventBus


class EventBusFactory(ABC):
	@abstractmethod
	def build(self) -> EventBus:
		pass
