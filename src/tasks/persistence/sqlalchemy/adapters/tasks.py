from datetime import datetime
from logging import Logger

from sqlalchemy import distinct
from sqlalchemy.orm import Session

from src.libs.hmi.querystring import Filter
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.tasks import Task
from src.tasks.persistence.ports import TaskDBPort
from src.tasks.persistence.sqlalchemy.querysets import TagQueryset, TaskQueryset

logger = Logger(__name__)


class TaskDB(TaskDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TaskQueryset()

    def tasks(
        self,
        session: Session,
        tenant_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks"""

        self.qs.select().from_filters(filters).tenants(tenant_ids)
        return session.execute(self.qs.statement).scalars().all()

    def tag_tasks(
        self,
        session: Session,
        tenant_ids: list[str],
        tag_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""

        self.qs.select().from_filters(filters).tenants(tenant_ids).tag(tag_id)
        return session.execute(self.qs.statement).scalars().all()

    def add_tags(
        self,
        session: Session,
        tenant_ids: list[str],
        task: Task,
        tag_ids: list[str],
    ) -> None:
        """Bulk add tags to tenant's task"""

        task = self.load(session=session, id=task.id)
        tag_qs = TagQueryset()
        tag_qs = tag_qs.select().tenants(tenant_ids).ids(tag_ids)
        tags = session.execute(tag_qs.statement).scalars().all()

        task.tags = tags

    def clean_tags(self, session: Session, task: Task) -> None:
        """Clean all associations with tags"""

        task = self.load(session=session, id=task.id)
        task.tags = []

    def delete_all_by_tenant(self, session, tenant_id: str) -> None:
        """Clean all tenant's tasks"""

        self.qs.delete().tenants(tenant_ids=[tenant_id])
        session.execute(self.qs.statement)

    def all_assigned_to_for_scheduled_between(
        self, session, start: datetime, end: datetime
    ) -> list[str]:
        """Return all distinct assigned_to ids in tasks list"""

        self.qs.select(distinct(Task.assigned_to)).scheduled_in(start=start, end=end)
        return session.execute(self.qs.statement).scalars().all()

    def get_tasks_assigned_to_and_scheduled_between(
        self, session, ids: list[str], start: datetime, end: datetime
    ) -> list[Task]:
        """Return all tasks assigned_to ids and scheduled between start and end"""

        self.qs.select().scheduled_in(start=start, end=end).where(
            Task.assigned_to.in_(ids)
        ).order_by(scheduled_at="ASC")
        return session.execute(self.qs.statement).scalars().all()
