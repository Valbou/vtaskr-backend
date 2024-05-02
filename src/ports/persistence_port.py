from abc import ABC, abstractmethod
from typing import Any, TypeVar

from .base_port import InjectablePort

TSessionPort = TypeVar("TSessionPort", bound="SessionPort")


class AbstractDBPort(ABC):
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


class SessionPort(ABC):
    def __enter__(self) -> TSessionPort:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()


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

    def register_repository(
        self, app_name: str, class_name: str, repository_instance: AbstractDBPort
    ) -> None:
        self._repository_registry[f"{app_name}:{class_name}"] = repository_instance

    def get_repository(self, app_name: str, class_name: str) -> AbstractDBPort | None:
        return self._repository_registry.get(f"{app_name}:{class_name}")
