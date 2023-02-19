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

	@property
	@abstractmethod
	def unique_identifier(self) -> str:
		return "event.{entity}.{use_case}.{event}"

	@property
	def body(self) -> Dict:
		return asdict(self)
