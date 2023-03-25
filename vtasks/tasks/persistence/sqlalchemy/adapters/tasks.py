from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.tasks.persistence.ports import AbstractTaskPort
from vtasks.tasks import Task


class TaskDB(AbstractTaskPort):
    def load(self, session: Session, id: str) -> Task:
        stmt = select(Task).where(Task.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, task: Task, autocommit: bool = True) -> True:
        session.add(task)
        if autocommit:
            session.commit()
        return True

    def delete(self, session: Session, task: Task, autocommit: bool = True) -> True:
        session.delete(task)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Task).where(Task.id == id).exists()).scalar()
