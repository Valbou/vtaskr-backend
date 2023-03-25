from abc import ABC, abstractmethod

from vtasks.base.persistence import AbstractPort
from vtasks.users import User


class AbstractUserPort(AbstractPort, ABC):
    @abstractmethod
    def find_login(self, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def update(self, user: User) -> bool:
        raise NotImplementedError()
