from infrastructure.event_buses.event_bus import EventBus
from infrastructure.event_buses.event_bus_factory import EventBusFactory


class KafkaEventBusFactory(EventBusFactory):
	def build(self) -> KafkaEventBus:
		return KafkaEventBus()
