from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.ports import AbstractDBPort
from src.users import Group


class GroupDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, user: Group) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def accessibles_by_user_with_permission(
        self,
        session,
        permission: Permissions,
        user_id: str,
        resource: Resources,
    ) -> list[str] | None:
        raise NotImplementedError()

    @abstractmethod
    def get_all_user_groups(
        self,
        session,
        user_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        raise NotImplementedError()
