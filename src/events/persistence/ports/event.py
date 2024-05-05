from abc import ABC, abstractmethod

from src.events.models import Event
from src.ports import AbstractDBPort


class EventDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def get_all(self, session) -> list[Event]:
        raise NotImplementedError()

    @abstractmethod
    def get_all_from_tenant(self, session, tenant_id: str) -> list[Event]:
        raise NotImplementedError()
