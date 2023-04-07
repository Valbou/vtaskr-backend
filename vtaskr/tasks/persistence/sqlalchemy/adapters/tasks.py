from typing import List, Optional

from sqlalchemy.orm import Session

from vtaskr.tasks import Task
from vtaskr.tasks.persistence.ports import AbstractTaskPort
from vtaskr.tasks.persistence.sqlalchemy.querysets import TaskQueryset


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

    def user_tasks(self, session: Session, user_id: str) -> List[Task]:
        # TODO: need a better control on where clause, limit and ordering
        self.task_qs.user(user_id)
        return session.execute(self.task_qs.statement.limit(100)).scalars().all()

    def user_tag_tasks(self, session: Session, user_id: str, tag_id: str) -> List[Task]:
        # TODO: need a better control on where clause, limit and ordering
        self.task_qs.user(user_id).tag(tag_id)
        return session.execute(self.task_qs.statement.limit(100)).scalars().all()
