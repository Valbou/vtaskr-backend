from abc import ABC, abstractmethod

from vtasks.users import User

from .base_ports import AbstractPort


class AbstractUserPort(AbstractPort, ABC):
    @abstractmethod
    def find_login(self, email: str) -> User:
        raise NotImplementedError()
