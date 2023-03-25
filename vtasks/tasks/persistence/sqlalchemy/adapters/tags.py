from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.tasks.persistence.ports import AbstractTagPort
from vtasks.tasks.models import Tag


class TagDB(AbstractTagPort):
    def load(self, session: Session, id: str) -> Tag:
        stmt = select(Tag).where(Tag.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, tag: Tag, autocommit: bool = True) -> True:
        session.add(tag)
        if autocommit:
            session.commit()
        return True

    def delete(self, session: Session, tag: Tag, autocommit: bool = True) -> True:
        session.delete(tag)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Tag).where(Tag.id == id).exists()).scalar()
