from abc import ABC, abstractmethod

from vtasks.base.persistence import AbstractPort
from vtasks.users import Token


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
