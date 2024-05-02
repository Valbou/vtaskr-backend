from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import Role


class RoleDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, user: Role) -> bool:
        raise NotImplementedError()
