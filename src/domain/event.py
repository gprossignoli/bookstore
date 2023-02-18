import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


def _get_new_uuid() -> str:
	return str(uuid.uuid4())


@dataclass
class Event(ABC):
	id: Optional[str] = field(init=False, default_factory=_get_new_uuid)

	@abstractmethod
	@property
	def unique_identifier(self) -> str:
		return "event.{entity}.{use_case}.{event}"
