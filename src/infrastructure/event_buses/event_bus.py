from abc import ABC, abstractmethod

from src.domain.event import Event


class EventBus(ABC):
	@abstractmethod
	def publish(self, event: Event) -> None:
		pass
