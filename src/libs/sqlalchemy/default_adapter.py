from sqlalchemy.orm import Session

from src.libs.sqlalchemy.queryset import Queryset
from src.ports import AbstractDBPort


class DefaultDB(AbstractDBPort):
    qs = Queryset(None)

    def load(
        self, session: Session, id: str, with_unique: bool = False
    ) -> object | None:
        """Load an object with id from database"""

        self.qs.select().id(id)
        if with_unique:
            result = session.scalars(self.qs.statement).unique().one_or_none()
        else:
            result = session.scalars(self.qs.statement).one_or_none()
        return result

    def save(self, session: Session, obj: object) -> None:
        """Save an object in database"""

        session.add(obj)

        return obj

    def bulk_save(
        self,
        session: Session,
        objs: list[object],
        number_per_loop: int = 500,
    ) -> None:
        """Save many objects in database in an optimized number of hits"""

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

        return objs

    def delete(self, session: Session, obj: object) -> None:
        """Delete an object from database"""

        session.delete(obj)

    def delete_by_id(self, session: Session, id: str) -> None:
        """Delete an object from database from id"""

        self.qs.delete().id(id)
        session.execute(self.qs.statement)

    def exists(self, session: Session, id: str) -> bool:
        """Check if an object exists in database"""

        self.qs.select().id(id)
        return session.query(self.qs.statement.exists()).scalar()
