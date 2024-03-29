from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.tasks import Tag


class AbstractTagPort(AbstractPort, ABC):
    @abstractmethod
    def tags(self, user_id: str) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def task_tags(self, user_id: str, task_id: str) -> list[Tag]:
        raise NotImplementedError()
