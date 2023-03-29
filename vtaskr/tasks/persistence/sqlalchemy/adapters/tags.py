from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from vtaskr.tasks.models import Tag, Task
from vtaskr.tasks.persistence.ports import AbstractTagPort


class TagDB(AbstractTagPort):
    def load(self, session: Session, id: str) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, tag: Tag, autocommit: bool = True):
        session.add(tag)
        if autocommit:
            session.commit()

    def delete(self, session: Session, tag: Tag, autocommit: bool = True):
        session.delete(tag)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Tag).where(Tag.id == id).exists()).scalar()

    def user_tags(self, session: Session, user_id: str) -> List[Tag]:
        # TODO: need a better control on where clause, limit and ordering
        stmt = select(Tag).where(Tag.user_id == user_id).limit(100)
        return session.execute(stmt).scalars().all()

    def user_task_tags(self, session: Session, user_id: str, task_id: str) -> List[Tag]:
        # TODO: need a better control on where clause, limit and ordering
        stmt = (
            select(Tag)
            .where(Tag.user_id == user_id, Tag.tasks.any(Task.id == task_id))
            .limit(100)
        )
        return session.execute(stmt).scalars().all()
