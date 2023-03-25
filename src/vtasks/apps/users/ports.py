from abc import ABC, abstractmethod


class AbstractPersistenceUserPort(ABC):
    @abstractmethod
    def load(self, id: str):
        raise NotImplementedError()

    @abstractmethod
    def save(self, item):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError()
