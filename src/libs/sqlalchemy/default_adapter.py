from sqlalchemy.orm import Session

from src.libs.sqlalchemy.queryset import Queryset

from .default_port import AbstractPort


class DefaultDB(AbstractPort):
    qs = Queryset(None)

    def load(self, session: Session, id: str) -> object | None:
        self.qs.id(id)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def save(self, session: Session, obj: object, autocommit: bool = True) -> None:
        session.add(obj)
        if autocommit:
            session.commit()

    def delete(self, session: Session, obj: object, autocommit: bool = True) -> None:
        session.delete(obj)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.qs.id(id)
        return session.query(self.qs.statement.exists()).scalar()
