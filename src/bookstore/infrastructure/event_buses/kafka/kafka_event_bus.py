from logging import Logger

from bookstore.domain.event import Event
from bookstore.infrastructure.event_buses import EventBus
from bookstore.infrastructure.event_buses.kafka.kafka_producer_factory import KafkaProducerFactory
from bookstore.infrastructure.event_buses.kafka.kafka_event_serializer import KafkaEventSerializer
from bookstore.infrastructure.event_buses.kafka.kafka_topics_manager import KafkaTopicsManager
from bookstore.infrastructure.event_buses.register_delivery_data import register_delivery_data
from bookstore.infrastructure.event_buses.register_publication_data import register_publication_data


class KafkaEventBus(EventBus):
	def __init__(self, logger: Logger):
		self.__logger = logger
		self.__topics_manager = KafkaTopicsManager()
		self.__kafka_producer = KafkaProducerFactory().build()
		self.__event_serializer = KafkaEventSerializer()

	def publish(self, event: Event) -> None:
		event_value = self.__event_serializer.serialize(event)

		try:
			self.__create_topic(event.unique_identifier)
		except Exception as e:
			self.__logger.error(f"Error creating the topic {event.unique_identifier}")
			raise e

		try:
			self.__publish_event(event=event, event_value=event_value)
		except Exception as e:
			raise e

	def __create_topic(self, event_identifier: str, partitions: int = 3, replication_factor: int = 3) -> None:
		self.__topics_manager.create_topic(topic_name=event_identifier, num_partitions=partitions,
										   replication_factor=replication_factor, config={"min.insync.replicas": 2})

	@register_publication_data
	def __publish_event(self, event: Event, event_value: str):
		self.__kafka_producer.produce(topic=event.unique_identifier, value=event_value, key=event.id,
									  on_delivery=self.__on_delivery)
		self.__kafka_producer.poll(timeout=10)

	@register_delivery_data
	def __on_delivery(self, err, msg) -> None:
		if err:
			self.__logger.warning(f"ERROR: Message {msg.value().decode('utf-8')} failed delivery: {err}")
		else:
			self.__logger.info(f"Event to topic {msg.topic()}: key = {msg.key().decode('utf-8')}")
