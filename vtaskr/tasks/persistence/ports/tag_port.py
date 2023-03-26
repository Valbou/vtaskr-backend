from abc import ABC, abstractmethod
from typing import List

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag, Task


class AbstractTagPort(AbstractPort, ABC):
    @abstractmethod
    def add_task(self, tag: Tag, task: Task):
        raise NotImplementedError()

    @abstractmethod
    def user_tags(self, user_id: str) -> List[Tag]:
        raise NotImplementedError()
