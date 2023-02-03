from sqlalchemy.orm import Session
from sqlalchemy import select

from src.vtasks.apps.users.ports import AbstractUserPort
from src.vtasks.apps.users.models import User


class UserDB(AbstractUserPort):
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
