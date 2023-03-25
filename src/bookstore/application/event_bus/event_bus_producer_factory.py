from abc import ABC, abstractmethod

from bookstore.application.event_bus import EventBusProducer


class EventBusProducerFactory(ABC):
	@abstractmethod
	def build(self) -> EventBusProducer:
		pass
