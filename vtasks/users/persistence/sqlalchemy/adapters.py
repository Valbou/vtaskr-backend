from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.sqlalchemy.database import SQLService, DBType
from vtasks.users.persistence.ports import AbstractUserPort
from vtasks.users.models import User


class UserDB(AbstractUserPort):
    def __init__(self, db_type: DBType) -> None:
        super().__init__()
        self.sql_service = SQLService(db_type)

    def get_session(self) -> Session:
        return self.sql_service.get_session()

    def load(self, session: Session, id: str) -> User:
        stmt = select(User).where(User.id == id)
        result = session.scalars(stmt).one_or_none()
        session.commit()
        return result

    def save(self, session: Session, user: User) -> True:
        session.add(user)
        session.commit()
        return True

    def delete(self, session: Session, user: User) -> True:
        session.delete(user)
        session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(User).where(User.id == id).exists()).scalar()
