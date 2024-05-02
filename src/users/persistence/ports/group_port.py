from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import Group


class GroupDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, user: Group) -> bool:
        raise NotImplementedError()
