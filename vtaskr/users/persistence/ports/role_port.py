from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.users import Role


class AbstractRolePort(AbstractPort, ABC):
    @abstractmethod
    def update(self, user: Role) -> bool:
        raise NotImplementedError()
