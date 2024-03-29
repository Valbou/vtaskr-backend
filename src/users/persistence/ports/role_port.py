from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.users import Role


class AbstractRolePort(AbstractPort, ABC):
    @abstractmethod
    def update(self, user: Role) -> bool:
        raise NotImplementedError()
