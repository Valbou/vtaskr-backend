from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from vtaskr.tasks import Task
from vtaskr.tasks.persistence.ports import AbstractTaskPort


class TaskDB(AbstractTaskPort):
    def load(self, session: Session, id: str) -> Optional[Task]:
        stmt = select(Task).where(Task.id == id)
        result = session.scalars(stmt).one_or_none()
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
        return session.query(select(Task).where(Task.id == id).exists()).scalar()

    def user_tasks(self, session: Session, user_id: str) -> List[Task]:
        # TODO: need a better control on where clause, limit and ordering
        stmt = select(Task).where(Task.user_id == user_id).limit(100)
        return session.execute(stmt).scalars().all()
