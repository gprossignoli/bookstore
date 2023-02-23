from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses import EventBus
from bookstore.infrastructure.event_buses.kafka.kafka_producer_factory import KafkaProducerFactory
from bookstore.infrastructure.event_buses.kafka.kafka_event_serializer import KafkaEventSerializer
from bookstore.infrastructure.event_buses.kafka.kafka_topics_manager import KafkaTopicsManager


class KafkaEventBus(EventBus):
	def __init__(self):
		self.__topics_manager = KafkaTopicsManager()
		self.__kafka_producer = KafkaProducerFactory().build()
		self.__event_serializer = KafkaEventSerializer()

# transacciones...
	def publish(self, event: Event) -> None:
		event_value = self.__event_serializer.serialize(event)

		self.__create_topic(event.unique_identifier)
		self.__kafka_producer.produce(topic=event.unique_identifier, value=event_value, on_delivery=self.__on_delivery)

	def __on_delivery(self, err, msg) -> None:
		if err:
			print('ERROR: Message failed delivery: {}'.format(err))
		else:
			print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
				topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

	def __create_topic(self, event_identifier: str, partitions: int = 3, replication_factor: int = 3) -> None:
		self.__topics_manager.create_topic(topic_name=event_identifier, num_partitions=partitions,
										   replication_factor=replication_factor, config={"min.insync.replicas": 2})
