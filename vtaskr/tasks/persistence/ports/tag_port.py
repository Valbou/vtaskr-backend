from abc import ABC

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag, Task


class AbstractTagPort(AbstractPort, ABC):
    def add_task(self, tag: Tag, task: Task) -> object:
        raise NotImplementedError()
