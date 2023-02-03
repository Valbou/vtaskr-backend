from abc import ABC, abstractmethod

from src.vtasks.database import SQLService, DBType


class AbstractModelPort(ABC):
    def __init__(self, db_type: DBType) -> None:
        super().__init__()
        self.sql_service = SQLService(db_type)

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
