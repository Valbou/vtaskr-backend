from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.users import RoleType


class AbstractRoleTypePort(AbstractPort, ABC):
    @abstractmethod
    def get_or_create(self, name: str, group_id: str) -> tuple[RoleType, bool]:
        raise NotImplementedError()
