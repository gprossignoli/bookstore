from confluent_kafka.admin import AdminClient

from bookstore.infrastructure.event_buses.kafka.kafka_client_configuration import (
    KafkaClientConfiguration,
)


class KafkaAdminFactory:
    def __init__(self) -> None:
        self.__admin_conf = KafkaClientConfiguration().base_configuration()

    def build(self) -> AdminClient:
        return AdminClient(self.__admin_conf)
