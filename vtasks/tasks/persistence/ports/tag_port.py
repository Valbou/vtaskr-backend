from abc import ABC

from vtasks.tasks import Task, Tag

from vtasks.base.persistence import AbstractPort


class AbstractTagPort(AbstractPort, ABC):
    def add_task(self, tag: Tag, task: Task) -> object:
        raise NotImplementedError()
