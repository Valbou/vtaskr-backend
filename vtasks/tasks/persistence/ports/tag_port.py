from abc import ABC

from vtasks.tasks import Task, Tag

from .base_ports import AbstractPort


class AbstractTagPort(AbstractPort, ABC):
    def add_task(self, tag: Tag, task: Task) -> object:
        raise NotImplementedError()
