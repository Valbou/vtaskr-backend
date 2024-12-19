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
    def all_exists(self, session, tenant_ids: list[str], tag_ids: list[str]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def tags_from_ids(
        self,
        session,
        tenant_ids: list[str],
        tag_ids: list[str],
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

    @abstractmethod
    def delete_all_by_tenant(self, session, tenant_id: str) -> None:
        """Clean all tenant's tags"""
        raise NotImplementedError()
