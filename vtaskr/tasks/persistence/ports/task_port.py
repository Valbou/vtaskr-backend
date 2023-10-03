from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Task


class AbstractTaskPort(AbstractPort, ABC):
    @abstractmethod
    def user_tasks(self, user_id: str) -> list[Task]:
        """Retrieve all user's tasks"""
        raise NotImplementedError()

    @abstractmethod
    def user_tag_tasks(self, user_id: str, tag_id: str) -> list[Task]:
        """Retrieve all user's tasks with this tag"""
        raise NotImplementedError()

    @abstractmethod
    def user_add_tags(self, user_id: str, task: Task, tags_id: list[str]):
        """Bulk add tags to user's task"""
        raise NotImplementedError()

    @abstractmethod
    def clean_tags(self, user_id: str, task: Task):
        """Clean all associations with tags"""
        raise NotImplementedError()
