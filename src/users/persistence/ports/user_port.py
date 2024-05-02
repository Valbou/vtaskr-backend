from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import User


class UserDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def find_login(self, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def clean_unused(self) -> User:
        raise NotImplementedError()

    @abstractmethod
    def update(self, user: User) -> bool:
        raise NotImplementedError()
