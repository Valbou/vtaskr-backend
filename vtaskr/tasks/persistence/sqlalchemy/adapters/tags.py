from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence.ports import AbstractTagPort
from vtaskr.tasks.persistence.sqlalchemy.querysets import TagQueryset


class TagDB(AbstractTagPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TagQueryset()

    def tags(
        self,
        session: Session,
        tenant_ids: list[str],
        filters: Optional[list[Filter]] = None,
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
        filters: Optional[list[Filter]] = None,
    ) -> list[Tag]:
        """Retrieve all tenant's tags for this task"""

        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.tenants(tenant_ids).task(task_id)

        return session.execute(self.qs.statement).scalars().all()
