from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.users import Group


class AbstractGroupPort(AbstractPort, ABC):
    @abstractmethod
    def update(self, user: Group) -> bool:
        raise NotImplementedError()
