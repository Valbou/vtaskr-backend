from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.users.models import RequestChange


class RequestChangeDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, request_change: RequestChange) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def find_request(self, session, email: str) -> RequestChange | None:
        raise NotImplementedError

    @abstractmethod
    def clean_history(self, session):
        raise NotImplementedError
