from abc import ABC, abstractmethod

from src.vtasks.apps.base.ports import AbstractModelPort


class AbstractUserPort(AbstractModelPort, ABC):
    @abstractmethod
    def load(self, id: str) -> object:
        raise NotImplementedError()

    @abstractmethod
    def save(self, item) -> object:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def exists(self, id: str) -> bool:
        raise NotImplementedError()
