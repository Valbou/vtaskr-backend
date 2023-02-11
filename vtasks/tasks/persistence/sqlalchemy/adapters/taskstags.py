from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.tasks.persistence.ports import AbstractTaskTagPort
from vtasks.tasks.models import TaskTag


class TaskTagDB(AbstractTaskTagPort):
    def load(self, session: Session, id: str) -> TaskTag:
        stmt = select(TaskTag).where(TaskTag.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, tasktag: TaskTag, autocommit: bool = True) -> True:
        session.add(tasktag)
        if autocommit:
            session.commit()
        return True

    def delete(
        self, session: Session, tasktag: TaskTag, autocommit: bool = True
    ) -> True:
        session.delete(tasktag)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, task_id: str, tag_id: str) -> bool:
        return session.query(
            select(TaskTag)
            .where(TaskTag.task_id == task_id, TaskTag.tag_id == tag_id)
            .exists()
        ).scalar()
