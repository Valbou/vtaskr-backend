from abc import ABC, abstractmethod

from vtaskr.base.persistence import AbstractPort
from vtaskr.tasks import Tag


class AbstractTagPort(AbstractPort, ABC):
    @abstractmethod
    def tenant_tags(self, tenant_id: str) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def tenant_task_tags(self, tenant_id: str, task_id: str) -> list[Tag]:
        raise NotImplementedError()
