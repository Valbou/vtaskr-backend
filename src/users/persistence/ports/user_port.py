from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.users import User


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
