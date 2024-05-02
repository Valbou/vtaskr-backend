from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.tasks import Tag


class TagDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def tags(self, user_id: str) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def task_tags(self, user_id: str, task_id: str) -> list[Tag]:
        raise NotImplementedError()
