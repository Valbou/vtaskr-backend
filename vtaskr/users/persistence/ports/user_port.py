from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.users import User


class AbstractUserPort(AbstractPort, ABC):
    @abstractmethod
    def find_login(self, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def clean_unused(self) -> User:
        raise NotImplementedError()

    @abstractmethod
    def update(self, user: User) -> bool:
        raise NotImplementedError()
