from bookstore.infrastructure.event_buses import EventBusFactory
from bookstore.infrastructure.event_buses.kafka import KafkaEventBus


class KafkaEventBusFactory(EventBusFactory):
	def build(self) -> KafkaEventBus:
		return KafkaEventBus()
