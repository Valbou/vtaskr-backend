from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.sqlalchemy.database import SQLService, DBType
from vtasks.users.persistence.ports import AbstractTokenPort
from vtasks.users.models import Token


class TokenDB(AbstractTokenPort):
    def __init__(self, db_type: DBType) -> None:
        super().__init__()
        self.sql_service = SQLService(db_type)

    def get_session(self) -> Session:
        return self.sql_service.get_session()

    def load(self, session: Session, id: str) -> Token:
        stmt = select(Token).where(Token.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, user: Token, autocommit: bool = True) -> True:
        session.add(user)
        if autocommit:
            session.commit()
        return True

    def delete(self, session: Session, user: Token, autocommit: bool = True) -> True:
        session.delete(user)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Token).where(Token.id == id).exists()).scalar()
