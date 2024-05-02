from abc import ABC, abstractmethod

from src.ports import AbstractDBPort


class RequestChangeDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def find_request(self, session, email: str):
        raise NotImplementedError

    @abstractmethod
    def clean_history(self, session):
        raise NotImplementedError
