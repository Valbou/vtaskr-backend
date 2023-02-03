from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from src.vtasks.database import SQLService, DBType


class AbstractModelPort(ABC):
    def __init__(self, db_type: DBType) -> None:
        super().__init__()
        self.sql_service = SQLService(db_type)

    def get_session(self) -> Session:
        return self.sql_service.get_session()

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
