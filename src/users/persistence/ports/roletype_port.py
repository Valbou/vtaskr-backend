from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.users import RoleType


class AbstractRoleTypePort(AbstractPort, ABC):
    @abstractmethod
    def get_or_create(self, name: str, group_id: str) -> tuple[RoleType, bool]:
        raise NotImplementedError()
