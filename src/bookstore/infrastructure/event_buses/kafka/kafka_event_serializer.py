import json

from bookstore.domain.event import Event


class KafkaEventSerializer:
	def serialize(self, event: Event) -> str:
		return json.dumps(event.body)
