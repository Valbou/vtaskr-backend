from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from vtasks.tasks.models import Tag
from vtasks.tasks.persistence.ports import AbstractTagPort


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
