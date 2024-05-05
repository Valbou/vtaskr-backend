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

        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.tenants(tenant_ids)

        return session.execute(self.qs.statement).scalars().all()

    def task_tags(
        self,
        session: Session,
        tenant_ids: list[str],
        task_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Tag]:
        """Retrieve all tenant's tags for this task"""

        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.tenants(tenant_ids).task(task_id)

        return session.execute(self.qs.statement).scalars().all()
