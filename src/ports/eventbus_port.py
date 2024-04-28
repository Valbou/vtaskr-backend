from abc import ABC, abstractmethod
from typing import Callable

from .base_port import InjectablePort


class EventBusPort(InjectablePort, ABC):
    @abstractmethod
    def emit(self, event_type: str, event: dict | object) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event_type: str, function: Callable):
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError
