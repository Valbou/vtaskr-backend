from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Task


class AbstractTaskPort(AbstractPort, ABC):
    @abstractmethod
    def tenant_tasks(self, tenant_id: str) -> list[Task]:
        """Retrieve all tenant's tasks"""
        raise NotImplementedError()

    @abstractmethod
    def tenant_tag_tasks(self, tenant_id: str, tag_id: str) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""
        raise NotImplementedError()

    @abstractmethod
    def tenant_add_tags(self, tenant_id: str, task: Task, tags_id: list[str]):
        """Bulk add tags to tenant's task"""
        raise NotImplementedError()

    @abstractmethod
    def clean_tags(self, tenant_id: str, task: Task):
        """Clean all associations with tags"""
        raise NotImplementedError()
