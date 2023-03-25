from abc import ABC, abstractmethod

from vtasks.users import User

from vtasks.base.persistence import AbstractPort


class AbstractUserPort(AbstractPort, ABC):
    @abstractmethod
    def find_login(self, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def update(self, user: User) -> True:
        raise NotImplementedError()
