from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import RoleType


class RoleTypeDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_or_create(self, name: str, group_id: str) -> tuple[RoleType, bool]:
        raise NotImplementedError()
