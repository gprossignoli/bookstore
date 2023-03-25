from typing import Iterable

from bookstore.application.repositories import UserRepository
from bookstore.domain.user_not_found_exception import UserNotFoundException
from bookstore.models.user import User


class SqlalchemyUserRepository(UserRepository):
    def get_or_fail(self, user_id: str) -> User:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotFoundException()

        return user

    def get_user_ids(self, max_users: int) -> Iterable[str]:
        data = User.query.limit(max_users).all()
        return [user.id for user in data]
