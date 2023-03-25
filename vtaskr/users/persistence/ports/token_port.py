from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.users import Token


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
