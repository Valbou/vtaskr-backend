from abc import ABC, abstractmethod
from datetime import datetime

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

    @abstractmethod
    def delete_all_by_tenant(self, session, tenant_id: str) -> None:
        """Clean all tenant's tasks"""
        raise NotImplementedError()

    @abstractmethod
    def all_assigned_to_for_scheduled_between(
        self, session, start: datetime, end: datetime
    ) -> list[str]:
        """Return all distinct assigned_to ids in tasks list"""
        raise NotImplementedError()

    @abstractmethod
    def get_tasks_assigned_to_and_scheduled_between(
        self, session, ids: list[str], start: datetime, end: datetime
    ) -> list[Task]:
        """Return all tasks assigned_to ids and scheduled between start and end"""
        raise NotImplementedError()
