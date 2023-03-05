from typing import Optional

from confluent_kafka.cimpl import NewTopic

from bookstore.infrastructure.event_buses.kafka.kafka_admin_factory import KafkaAdminFactory


class KafkaTopicsManager:
	def __init__(self):
		self.__kafka_admin = KafkaAdminFactory().build()

	def create_topic(
			self, topic_name: str, num_partitions: int, replication_factor: int, config: Optional[dict] = None
	) -> None:
		topic_to_create = self.__create_topic_config(config, num_partitions, replication_factor, topic_name)

		cluster_metadata = self.__kafka_admin.list_topics()

		topic_data = cluster_metadata.topics.get(topic_name)
		if topic_data is None:
			self.__kafka_admin.create_topics([topic_to_create])

	def __create_topic_config(self, config, num_partitions, replication_factor, topic_name) -> NewTopic:
		if config is not None:
			return NewTopic(
				topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor, config=config
			)

		return NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
