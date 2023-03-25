from abc import ABC

from vtasks.base.persistence import AbstractPort
from vtasks.tasks import Tag, Task


class AbstractTagPort(AbstractPort, ABC):
    def add_task(self, tag: Tag, task: Task) -> object:
        raise NotImplementedError()
