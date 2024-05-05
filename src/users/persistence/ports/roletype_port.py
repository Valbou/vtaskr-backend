from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.ports import AbstractDBPort
from src.users.models import RoleType


class RoleTypeDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_or_create(self, session, roletype: RoleType) -> tuple[RoleType, bool]:
        raise NotImplementedError()

    @abstractmethod
    def get_a_user_roletype(
        self, session, roletype_id: str, group_ids: list[str]
    ) -> RoleType:
        raise NotImplementedError()

    @abstractmethod
    def get_all_user_roletypes(
        self,
        session,
        group_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[RoleType]:
        raise NotImplementedError()
