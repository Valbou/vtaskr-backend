from abc import ABC, abstractmethod
from typing import List

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Task


class AbstractTaskPort(AbstractPort, ABC):
    @abstractmethod
    def user_tasks(self, user_id: str) -> List[Task]:
        raise NotImplementedError()

    @abstractmethod
    def user_tag_tasks(self, user_id: str, tag_id: str) -> List[Task]:
        raise NotImplementedError()
