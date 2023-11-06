from abc import ABC, abstractmethod

from src.base.persistence import AbstractPort
from src.users import Role


class AbstractRolePort(AbstractPort, ABC):
    @abstractmethod
    def update(self, user: Role) -> bool:
        raise NotImplementedError()
