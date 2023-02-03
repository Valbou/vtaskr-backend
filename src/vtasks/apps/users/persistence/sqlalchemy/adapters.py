from sqlalchemy.orm import Session

from src.vtasks.apps.users.ports import AbstractUserPort
from src.vtasks.apps.users.models import User


class UserDB(AbstractUserPort):
    def load(self, id: str) -> User:
        pass

    def save(self, user: User) -> User:
        with Session(self.sql_service.get_engine()) as session:
            session.add(user)
            session.commit()
        return user

    def delete(self, id: str) -> bool:
        pass

    def exists(self, id: str) -> bool:
        pass
