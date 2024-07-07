from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.ports import AbstractDBPort
from src.users.models import Role


class RoleDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, user: Role) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_a_user_role(
        self, session, user_id: str, role_id: str, group_ids: list[str]
    ) -> Role | None:
        raise NotImplementedError()

    @abstractmethod
    def get_all_user_roles(
        self,
        session,
        user_id: str,
        group_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Role]:
        raise NotImplementedError()

    @abstractmethod
    def get_group_roles(self, session, group_id: str) -> list[Role]:
        raise NotImplementedError()
