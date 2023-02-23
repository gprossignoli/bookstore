from typing import Optional

from confluent_kafka.admin import ClusterMetadata
from confluent_kafka.cimpl import NewTopic

from bookstore.infrastructure.event_buses.kafka.kafka_admin_factory import KafkaAdminFactory


class KafkaTopicsManager:
	def __init__(self):
		self.__kafka_admin = KafkaAdminFactory().build()

	def create_topic(self, topic_name: str, num_partitions: int, replication_factor: int, config: Optional[dict] = None) -> None:
		topic_to_create = self.__create_topic_config(config, num_partitions, replication_factor, topic_name)

		topic_metadata = self.__kafka_admin.list_topics(topic=topic_name)

		topic_doesnt_exists_already = topic_metadata.error is not None
		topic_already_exists = topic_metadata.config == topic_to_create.config

		if topic_doesnt_exists_already is False:
			self.__kafka_admin.create_topics([topic_to_create])
		elif topic_already_exists:
			pass
		else:
			raise Exception('Topic exists with different configuration')

	def __create_topic_config(self, config, num_partitions, replication_factor, topic_name) -> NewTopic:
		if config is not None:
			return NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor,
							config=config)

		return NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
