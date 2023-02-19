from abc import ABC, abstractmethod

from bookstore.domain.event import Event


class EventBus(ABC):
	@abstractmethod
	def publish(self, event: Event) -> None:
		pass
