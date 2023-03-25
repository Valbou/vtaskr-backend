from src.vtasks.apps.base.ports import AbstractModelPort
from src.vtasks.apps.users.models import User


class UserDB(AbstractModelPort):
    def load(self, id: str) -> User:
        pass

    def save(self, user: User) -> User:
        pass

    def delete(self, id: str) -> bool:
        pass
