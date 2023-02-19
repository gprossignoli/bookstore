from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses import EventBus
from bookstore.infrastructure.event_buses.kafka.kafka_producer_factory import KafkaProducerFactory
from bookstore.infrastructure.event_buses.kafka.kafka_event_serializer import KafkaEventSerializer


class KafkaEventBus(EventBus):
	def __init__(self):
		self.__kafka_producer = KafkaProducerFactory().build()
		self.__event_serializer = KafkaEventSerializer()

	def publish(self, event: Event) -> None:
		event_value = self.__event_serializer.serialize(event)
		self.__kafka_producer.produce(topic=event.unique_identifier, value=event_value, on_delivery=self.__on_delivery)

	def __on_delivery(self, err, msg) -> None:
		if err:
			print('ERROR: Message failed delivery: {}'.format(err))
		else:
			print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
				topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
