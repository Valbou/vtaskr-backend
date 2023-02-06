from abc import ABC, abstractmethod

from vtasks.users import Token

from .base_ports import AbstractPort


class AbstractTokenPort(AbstractPort, ABC):
    @abstractmethod
    def get_token(self, token: str) -> Token:
        raise NotImplementedError()
