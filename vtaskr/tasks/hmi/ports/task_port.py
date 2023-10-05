from abc import ABC, abstractmethod
from typing import Optional

from vtaskr.tasks.models import Task


class AbstractTaskPort(ABC):
    @abstractmethod
    def get_tenant_tasks(self, tenant_id: str) -> list[dict]:
        raise NotImplementedError()

    def get_tenant_task(self, tenant_id: str, task_id: str) -> Optional[Task]:
        raise NotImplementedError()

    def get_tenant_tag_tasks(self, tenant_id: str, tag_id: str) -> list[Task]:
        raise NotImplementedError()

    def update_tenant_task(self, tenant_id: str, task: Task):
        raise NotImplementedError()

    def delete_tenant_task(self, tenant_id: str, task: Task):
        raise NotImplementedError()
