from abc import ABC

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag, Task


class AbstractTaskPort(AbstractPort, ABC):
    def add_tag(self, task: Task, tag: Tag) -> object:
        raise NotImplementedError()
