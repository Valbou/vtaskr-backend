from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import Token


class TokenDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_token(self, token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def activity_update(self, token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def clean_expired(self) -> int:
        raise NotImplementedError()
