from abc import ABC

from vtasks.tasks import Task, Tag

from .base_ports import AbstractPort


class AbstractTaskPort(AbstractPort, ABC):
    def add_tag(self, task: Task, tag: Tag) -> object:
        raise NotImplementedError()
