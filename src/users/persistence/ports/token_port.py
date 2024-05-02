from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users import Token


class TokenDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_token(self, session, sha_token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def activity_update(self, session, token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def clean_expired(self, session) -> int:
        raise NotImplementedError()
