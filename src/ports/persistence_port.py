from abc import ABC, abstractmethod
from typing import Any, TypeVar

from .base_port import InjectablePort

TSessionPort = TypeVar("TSessionPort", bound="SessionPort")


class AbstractDBPort(ABC):
    @abstractmethod
    def load(self, session, id: str) -> object | None:
        raise NotImplementedError()

    @abstractmethod
    def save(self, session, obj) -> object:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, session, obj) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, session, id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def exists(self, session, id: str) -> bool:
        raise NotImplementedError()


class SessionPort(ABC):
    def __enter__(self) -> TSessionPort:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class PersistencePort(InjectablePort, ABC):
    _repository_registry: dict[str, AbstractDBPort]

    @abstractmethod
    def get_database_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_engine(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_session(self) -> SessionPort:
        raise NotImplementedError

    def _compose_index(self, app_name: str, class_name: str) -> str:
        return f"{app_name}:{class_name}"

    def register_repository(
        self, app_name: str, class_name: str, repository_instance: AbstractDBPort
    ) -> None:
        index_name = self._compose_index(app_name, class_name)
        self._repository_registry[index_name] = repository_instance

    def get_repository(self, app_name: str, class_name: str) -> AbstractDBPort | None:
        index_name = self._compose_index(app_name, class_name)
        return self._repository_registry.get(index_name)
