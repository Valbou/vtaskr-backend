from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.ports import AbstractDBPort
from src.tasks import Task


class TaskDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def tasks(
        self,
        session,
        tenant_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks"""
        raise NotImplementedError()

    @abstractmethod
    def tag_tasks(
        self,
        session,
        tenant_ids: list[str],
        tag_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""
        raise NotImplementedError()

    @abstractmethod
    def add_tags(
        self, session, tenant_ids: list[str], task: Task, tag_ids: list[str]
    ) -> None:
        """Bulk add tags to tenant's task"""
        raise NotImplementedError()

    @abstractmethod
    def clean_tags(self, session, task: Task) -> None:
        """Clean all associations with tags"""
        raise NotImplementedError()
