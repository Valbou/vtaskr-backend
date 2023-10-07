from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.base.persistence import AbstractPort
from vtaskr.libs.sqlalchemy.queryset import Queryset


class DefaultDB(AbstractPort):
    qs = Queryset(None)

    def load(self, session: Session, id: str) -> Optional[object]:
        self.qs.id(id)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def save(self, session: Session, obj: object, autocommit: bool = True):
        session.add(obj)
        if autocommit:
            session.commit()

    def delete(self, session: Session, obj: object, autocommit: bool = True):
        session.delete(obj)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.qs.id(id)
        return session.query(self.qs.statement.exists()).scalar()
