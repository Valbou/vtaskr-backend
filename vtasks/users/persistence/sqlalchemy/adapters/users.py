from sqlalchemy.orm import Session
from sqlalchemy import select

from vtasks.users.persistence.ports import AbstractUserPort
from vtasks.users.models import User


class UserDB(AbstractUserPort):
    def load(self, session: Session, id: str) -> User:
        stmt = select(User).where(User.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def save(self, session: Session, user: User, autocommit: bool = True) -> True:
        session.add(user)
        if autocommit:
            session.commit()
        return True

    def delete(self, session: Session, user: User, autocommit: bool = True) -> True:
        session.delete(user)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(User).where(User.id == id).exists()).scalar()

    def find_login(self, session: Session, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result = session.scalars(stmt).one_or_none()
        return result
