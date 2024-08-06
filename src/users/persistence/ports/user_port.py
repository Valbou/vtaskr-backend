from abc import ABC, abstractmethod

from src.libs.iam.constants import Permissions
from src.ports import AbstractDBPort
from src.users.models import User


class UserDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, user: User) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def find_user_by_email(self, session, email: str) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    def clean_unused(self, session) -> None:
        raise NotImplementedError()

    @abstractmethod
    def has_permissions(
        self,
        session,
        id: str,
        resource: str,
        permission: Permissions,
        group_id: str,
    ) -> bool:
        raise NotImplementedError()
