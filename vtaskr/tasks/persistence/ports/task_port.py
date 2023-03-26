from abc import ABC, abstractmethod
from typing import List

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag, Task


class AbstractTaskPort(AbstractPort, ABC):
    @abstractmethod
    def add_tag(self, task: Task, tag: Tag):
        raise NotImplementedError()

    @abstractmethod
    def user_tasks(self, user_id: str) -> List[Task]:
        raise NotImplementedError()
