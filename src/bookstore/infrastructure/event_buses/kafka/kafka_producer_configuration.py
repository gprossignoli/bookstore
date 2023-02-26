from typing import Dict

from bookstore.infrastructure.event_buses.kafka.kafka_client_configuration import KafkaClientConfiguration
from bookstore.infrastructure.event_buses.kafka .kafka_qos import KafkaQos


class KafkaProducerConfiguration(KafkaClientConfiguration):

	def exactly_once_configuration(self) -> Dict:
		extended_config = super().base_configuration()
		extended_config["acks"] = KafkaQos.AT_LEAST_ONCE_ALL_BROKERS_ACKNOWLEDGE.value
		extended_config["enable.idempotence"] = True

		return extended_config

	def at_most_once_configuration(self) -> Dict:
		extended_config = super().base_configuration()
		extended_config["acks"] = KafkaQos.AT_MOST_ONCE.value

		return extended_config

	def at_least_once_only_leader_configuration(self) -> Dict:
		extended_config = super().base_configuration()
		extended_config["acks"] = KafkaQos.AT_LEAST_ONCE_ONLY_LEADER_ACKNOWLEDGE.value
		extended_config["enable.idempotence"] = False

		return extended_config

	def at_least_once_all_brokers_configuration(self) -> Dict:
		extended_config = super().base_configuration()
		extended_config["acks"] = KafkaQos.AT_LEAST_ONCE_ALL_BROKERS_ACKNOWLEDGE.value
		extended_config["enable.idempotence"] = False

		return extended_config
