from models.user import User


class UserNotFoundException(Exception):
	pass


class UserRepository:
	def get_or_fail(self, user_id: str) -> User:
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			raise UserNotFoundException()

		return user
