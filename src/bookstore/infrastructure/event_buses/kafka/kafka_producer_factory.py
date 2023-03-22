from confluent_kafka import Producer

from bookstore.infrastructure.event_buses.kafka.kafka_producer_configuration import (
    KafkaProducerConfiguration,
)


class KafkaProducerFactory:
    def __init__(self) -> None:
        self.__producer_conf = KafkaProducerConfiguration().exactly_once_configuration()

    def build(self) -> Producer:
        return Producer(self.__producer_conf)
