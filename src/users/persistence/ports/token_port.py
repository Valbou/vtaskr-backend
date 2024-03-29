from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.users import Token


class AbstractTokenPort(AbstractPort, ABC):
    @abstractmethod
    def get_token(self, token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def activity_update(self, token: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def clean_expired(self) -> int:
        raise NotImplementedError()
