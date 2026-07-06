from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    def get_by_email(self, email: str):
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def get_by_username(self, username: str):
        statement = select(User).where(User.username == username)

        return self.db.scalar(statement)