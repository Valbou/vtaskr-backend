from abc import ABC, abstractmethod

from src.ports import AbstractDBPort


class RequestChangeDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def clean_history(self):
        raise NotImplementedError

    @abstractmethod
    def find_request(self):
        raise NotImplementedError
