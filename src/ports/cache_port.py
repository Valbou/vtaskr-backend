from abc import ABC, abstractmethod
from typing import Any, ContextManager

from .base_port import InjectablePort


class CachePort(InjectablePort, ABC):
    @abstractmethod
    def get_database_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_engine(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_session(self) -> ContextManager:
        raise NotImplementedError
