from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.users import Group


class AbstractGroupPort(AbstractPort, ABC):
    @abstractmethod
    def update(self, user: Group) -> bool:
        raise NotImplementedError()
