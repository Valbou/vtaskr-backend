from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from vtaskr.users.models import User
from vtaskr.users.persistence.ports import AbstractUserPort


class UserDB(AbstractUserPort):
    def load(self, session: Session, id: str) -> Optional[User]:
        stmt = select(User).where(User.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def update(self, session: Session, user: User, autocommit: bool = True):
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                hash_password=user.hash_password,
            )
        )
        session.execute(stmt)
        if autocommit:
            session.commit()

    def save(self, session: Session, user: User, autocommit: bool = True):
        session.add(user)
        if autocommit:
            session.commit()

    def delete(self, session: Session, user: User, autocommit: bool = True):
        session.delete(user)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(User).where(User.id == id).exists()).scalar()

    def find_login(self, session: Session, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = session.scalars(stmt).one_or_none()
        return result
