import inspect
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, ClassVar


def _get_new_uuid() -> str:
	return str(uuid.uuid4())


@dataclass(frozen=True)
class Event(ABC):
	DATE_TIME_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M:%S.%f"
	id: Optional[str] = field(init=False, default_factory=_get_new_uuid)
	created_at: str = field(
		init=False, default_factory=lambda: datetime.strftime(datetime.now(), Event.DATE_TIME_FORMAT)
	)

	@classmethod
	@abstractmethod
	def unique_identifier(cls) -> str:
		return "event.{entity}.{use_case}.{event}"

	@property
	def body(self) -> Dict:
		return asdict(self)

	@classmethod
	def reconstruct(cls, event_id: str, created_at: str, payload: dict) -> "Event":
		instance = cls.__from_dict(payload)

		object.__setattr__(instance, "id", event_id)
		object.__setattr__(instance, "created_at", created_at)
		return instance

	@classmethod
	def __from_dict(cls, data: Dict) -> "Event":
		expected_params = inspect.signature(cls).parameters
		actual_params = {
			key: value for key, value in data.items() if key in expected_params
		}
		return cls(**actual_params)  # type: ignore[call-arg]
