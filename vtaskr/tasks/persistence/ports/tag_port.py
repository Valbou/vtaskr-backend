from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag


class AbstractTagPort(AbstractPort, ABC):
    @abstractmethod
    def user_tags(self, user_id: str) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def user_task_tags(self, user_id: str, task_id: str) -> list[Tag]:
        raise NotImplementedError()
