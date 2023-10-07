from logging import Logger
from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.tasks import Task
from vtaskr.tasks.persistence.ports import AbstractTaskPort
from vtaskr.tasks.persistence.sqlalchemy.querysets import TagQueryset, TaskQueryset

logger = Logger(__name__)


class TaskDB(AbstractTaskPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TaskQueryset()

    def tasks(
        self,
        session: Session,
        tenant_ids: list[str],
        filters: Optional[list[Filter]] = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks"""

        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.tenants(tenant_ids)
        return session.execute(self.qs.statement).scalars().all()

    def tag_tasks(
        self,
        session: Session,
        tenant_ids: list[str],
        tag_id: str,
        filters: Optional[list[Filter]] = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""

        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.tenants(tenant_ids).tag(tag_id)
        return session.execute(self.qs.statement).scalars().all()

    def add_tags(
        self,
        session: Session,
        tenant_ids: list[str],
        task: Task,
        tag_ids: list[str],
        autocommit: bool = True,
    ):
        """Bulk add tags to tenant's task"""

        tag_qs = TagQueryset()
        tag_qs = tag_qs.tenants(tenant_ids).ids(tag_ids)
        tags = session.execute(tag_qs.statement).scalars().all()

        task.tags = tags
        if autocommit:
            session.commit()

    def clean_tags(self, session: Session, task: Task, autocommit: bool = True):
        """Clean all associations with tags"""

        task.tags = []
        if autocommit:
            session.commit()
