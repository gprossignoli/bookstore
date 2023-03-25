from abc import abstractmethod, ABC
from typing import Iterable

from bookstore.models.user import User


class UserRepository(ABC):
	@abstractmethod
	def get_or_fail(self, user_id: str) -> User:
		pass

	@abstractmethod
	def get_user_ids(self, max_users: int) -> Iterable[str]:
		pass
