from domain.event import Event
from infrastructure.event_buses.event_bus import EventBus


class KafkaEventBus(EventBus):
	def __init__(self):
		self.__kafka_producer = KafkaProducerFactory().build()

	def publish(self, event: Event) -> None:
		pass
