from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.ports import AbstractDBPort
from src.users.models import Right


class RightDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_all_user_rights(
        self,
        session,
        group_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Right]:
        raise NotImplementedError()

    @abstractmethod
    def get_a_user_right(
        self, session, user_id: str, right_id: str, group_ids: list[str]
    ) -> Right | None:
        raise NotImplementedError()
