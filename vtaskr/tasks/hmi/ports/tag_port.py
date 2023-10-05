from abc import ABC, abstractmethod
from typing import Optional

from vtaskr.tasks.models import Tag


class AbstractTagPort(ABC):
    @abstractmethod
    def get_tenant_tags(self, tenant_id: str) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def get_tenant_tag(self, tenant_id: str, tag_id: str) -> Optional[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def get_tenant_task_tags(self, tenant_id: str, task_id: str) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def update_tenant_tag(self, tenant_id: str, tag: Tag):
        raise NotImplementedError()

    @abstractmethod
    def delete_tenant_tag(self, tenant_id: str, tag: Tag):
        raise NotImplementedError()
