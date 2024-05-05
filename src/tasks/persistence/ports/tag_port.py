from abc import ABC, abstractmethod

from src.libs.hmi.querystring import Filter
from src.ports import AbstractDBPort
from src.tasks import Tag


class TagDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def tags(
        self,
        session,
        tenant_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def task_tags(
        self,
        session,
        tenant_ids: list[str],
        task_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Tag]:
        raise NotImplementedError()
