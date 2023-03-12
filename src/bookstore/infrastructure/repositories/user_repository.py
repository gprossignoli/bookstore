from typing import Sequence

from bookstore.models.user import User


class UserNotFoundException(Exception):
	pass


class UserRepository:
	def get_or_fail(self, user_id: str) -> User:
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			raise UserNotFoundException()

		return user

	def get_user_ids(self, max_users: int) -> Sequence:
		data = User.query.limit(max_users).all()
		return [user.id for user in data]
