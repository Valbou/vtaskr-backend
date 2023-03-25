from abc import ABC

from vtasks.base.persistence import AbstractPort
from vtasks.tasks import Tag, Task


class AbstractTaskPort(AbstractPort, ABC):
    def add_tag(self, task: Task, tag: Tag) -> object:
        raise NotImplementedError()
