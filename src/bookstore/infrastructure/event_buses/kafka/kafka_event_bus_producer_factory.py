from bookstore import settings
from bookstore.application.event_bus import EventBusProducerFactory
from bookstore.infrastructure.event_buses.kafka import KafkaEventBusProducer


class KafkaEventBusProducerFactory(EventBusProducerFactory):
	def build(self) -> KafkaEventBusProducer:
		return KafkaEventBusProducer(logger=settings.logger)
