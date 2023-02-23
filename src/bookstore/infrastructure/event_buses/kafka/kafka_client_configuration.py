from typing import List

from bookstore import settings


class KafkaClientConfiguration:
	def __init__(self):
		self.__bootstrap_servers: List[str] = settings.KAFKA_SERVERS
		self.__client_id: str = settings.KAFKA_CLIENT_ID
		self._base_configuration = {}

	def base_configuration(self):
		self._base_configuration = {
			"bootstrap.servers": self.__bootstrap_servers,
			"client.id": self.__client_id,
		}

		return self._base_configuration
