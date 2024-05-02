from abc import ABC, abstractmethod

from src.ports import AbstractDBPort
from src.tasks import Task


class TaskDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def tasks(self, user_id: str) -> list[Task]:
        """Retrieve all tenant's tasks"""
        raise NotImplementedError()

    @abstractmethod
    def tag_tasks(self, user_id: str, tag_id: str) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""
        raise NotImplementedError()

    @abstractmethod
    def add_tags(self, user_id: str, task: Task, tags_id: list[str]):
        """Bulk add tags to tenant's task"""
        raise NotImplementedError()

    @abstractmethod
    def clean_tags(self, user_id: str, task: Task):
        """Clean all associations with tags"""
        raise NotImplementedError()
