from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.tasks import Task
from vtaskr.tasks.persistence.ports import AbstractTaskPort
from vtaskr.tasks.persistence.sqlalchemy.querysets import TagQueryset, TaskQueryset


class TaskDB(AbstractTaskPort):
    def __init__(self) -> None:
        super().__init__()
        self.task_qs = TaskQueryset()

    def load(self, session: Session, id: str) -> Optional[Task]:
        self.task_qs.id(id)
        result = session.scalars(self.task_qs.statement).one_or_none()
        return result

    def save(self, session: Session, task: Task, autocommit: bool = True):
        session.add(task)
        if autocommit:
            session.commit()

    def delete(self, session: Session, task: Task, autocommit: bool = True):
        session.delete(task)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.task_qs.id(id)
        return session.query(self.task_qs.statement.exists()).scalar()

    def tenant_tasks(
        self, session: Session, tenant_id: str, filters: Optional[list[Filter]] = None
    ) -> list[Task]:
        """Retrieve all tenant's tasks"""

        filters = filters or []
        if filters:
            self.task_qs.from_filters(filters)

        self.task_qs.tenant(tenant_id)
        return session.execute(self.task_qs.statement).scalars().all()

    def tenant_tag_tasks(
        self,
        session: Session,
        tenant_id: str,
        tag_id: str,
        filters: Optional[list[Filter]] = None,
    ) -> list[Task]:
        """Retrieve all tenant's tasks with this tag"""

        filters = filters or []
        if filters:
            self.task_qs.from_filters(filters)

        self.task_qs.tenant(tenant_id).tag(tag_id)
        return session.execute(self.task_qs.statement).scalars().all()

    def tenant_add_tags(
        self,
        session: Session,
        tenant_id: str,
        task: Task,
        tags_id: list[str],
        autocommit: bool = True,
    ):
        """Bulk add tags to tenant's task"""

        tag_qs = TagQueryset()
        tag_qs = tag_qs.tenant(tenant_id).ids(tags_id)
        tags = session.execute(tag_qs.statement).scalars().all()

        task.tags = tags
        if autocommit:
            session.commit()

    def clean_tags(
        self, session: Session, tenant_id: str, task: Task, autocommit: bool = True
    ):
        """Clean all associations with tags"""

        task.tags = []
        if autocommit:
            session.commit()
