from typing import List, Dict

from bookstore import settings
from bookstore.infrastructure.event_buses.kafka .kafka_qos import KafkaQos


class KafkaProducerConfiguration:
	def __init__(self):
		self.__bootstrap_servers: List[str] = settings.KAFKA_SERVERS
		self.__client_id: str = settings.KAFKA_CLIENT_ID

	def exactly_once_configuration(self) -> Dict:
		return {"bootstrap.servers": self.__bootstrap_servers,
				"client.id": self.__client_id,
				"acks": KafkaQos.AT_LEAST_ONCE_ALL_BROKERS_ACKNOWLEDGE.value,
				"enable.idempotence": True}

	def at_most_once_configuration(self) -> Dict:
		return {"bootstrap.servers": self.__bootstrap_servers,
				"client.id": self.__client_id,
				"acks": KafkaQos.AT_MOST_ONCE.value
				}

	def at_least_once_only_leader_configuration(self) -> Dict:
		return {"bootstrap.servers": self.__bootstrap_servers,
				"client.id": self.__client_id,
				"acks": KafkaQos.AT_LEAST_ONCE_ONLY_LEADER_ACKNOWLEDGE.value,
				"enable.idempotence": False}

	def at_least_once_all_brokers_configuration(self) -> Dict:
		return {"bootstrap.servers": self.__bootstrap_servers,
				"client.id": self.__client_id,
				"acks": KafkaQos.AT_LEAST_ONCE_ALL_BROKERS_ACKNOWLEDGE.value,
				"enable.idempotence": False}
