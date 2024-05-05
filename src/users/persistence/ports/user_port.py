from abc import ABC, abstractmethod

from src.libs.iam.constants import Permissions, Resources
from src.ports import AbstractDBPort
from src.users.models import User


class UserDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, user: User) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def find_user_by_email(self, session, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def clean_unused(self, session) -> User:
        raise NotImplementedError()

    @abstractmethod
    def has_permissions(
        self,
        session,
        id: str,
        resource: Resources,
        permission: Permissions,
        group_id: str,
    ) -> bool:
        raise NotImplementedError()
