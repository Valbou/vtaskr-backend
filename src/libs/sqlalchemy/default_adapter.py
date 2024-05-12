from sqlalchemy.orm import Session

from src.libs.sqlalchemy.queryset import Queryset
from src.ports import AbstractDBPort


class DefaultDB(AbstractDBPort):
    qs = Queryset(None)

    def load(
        self, session: Session, id: str, with_unique: bool = False
    ) -> object | None:
        self.qs.select().id(id)
        if with_unique:
            result = session.scalars(self.qs.statement).unique().one_or_none()
        else:
            result = session.scalars(self.qs.statement).one_or_none()
        return result

    def save(self, session: Session, obj: object) -> None:
        session.add(obj)

    def bulk_save(
        self,
        session: Session,
        objs: list[object],
        number_per_loop: int = 500,
    ) -> None:
        objs_size = len(objs)
        pages = objs_size // number_per_loop + 1
        for p in range(pages):
            start = p * number_per_loop
            end = p * number_per_loop + number_per_loop
            if start < objs_size:
                if end > objs_size:
                    session.add_all(objs[start:])
                else:
                    session.add_all(objs[start:end])
                session.flush()

    def delete(self, session: Session, obj: object) -> None:
        session.delete(obj)

    def exists(self, session: Session, id: str) -> bool:
        self.qs.select().id(id)
        return session.query(self.qs.statement.exists()).scalar()
