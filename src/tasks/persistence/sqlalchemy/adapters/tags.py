from sqlalchemy.orm import Session

from src.libs.hmi.querystring import Filter
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.tasks.models import Tag
from src.tasks.persistence import TagDBPort
from src.tasks.persistence.sqlalchemy.querysets import TagQueryset


class TagDB(TagDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TagQueryset()

    def tags(
        self,
        session: Session,
        tenant_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Tag]:
        """Retrieve all tenant's tags"""

        self.qs.select().from_filters(filters).tenants(tenant_ids)

        return session.execute(self.qs.statement).scalars().all()

    def all_exists(self, session, tenant_ids: list[str], tag_ids: list[str]) -> bool:
        """Check if all tags exists for tenants"""

        self.qs.select().where(Tag.id.in_(tag_ids)).tenants(tenant_ids)

        return session.execute(self.qs.statement.exists()).scalars()

    def tags_from_ids(
        self,
        session: Session,
        tenant_ids: list[str],
        tag_ids: list[str],
    ) -> list[Tag]:
        """Retrieve all tenant's tags in tag_ids"""

        self.qs.select().where(Tag.id.in_(tag_ids)).tenants(tenant_ids)

        return session.execute(self.qs.statement).scalars().all()

    def task_tags(
        self,
        session: Session,
        tenant_ids: list[str],
        task_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Tag]:
        """Retrieve all tenant's tags for this task"""

        self.qs.select().from_filters(filters).tenants(tenant_ids).task(task_id)

        return session.execute(self.qs.statement).scalars().all()

    def delete_all_by_tenant(self, session, tenant_id: str) -> None:
        """Clean all tenant's tags"""

        self.qs.delete().tenants(tenant_ids=[tenant_id])
        session.execute(self.qs.statement)
