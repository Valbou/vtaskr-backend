from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.users.models import User
from vtaskr.users.persistence.ports import AbstractUserPort
from vtaskr.users.persistence.sqlalchemy.querysets import UserQueryset


class UserDB(AbstractUserPort):
    def __init__(self) -> None:
        super().__init__()
        self.user_qs = UserQueryset()

    def load(self, session: Session, id: str) -> Optional[User]:
        self.user_qs.id(id)
        result = session.scalars(self.user_qs.statement).one_or_none()
        return result

    def update(self, session: Session, user: User, autocommit: bool = True):
        self.user_qs.update().id(user.id).values(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hash_password=user.hash_password,
        )

        session.execute(self.user_qs.statement)
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
        self.user_qs.id(id)
        return session.query(self.user_qs.statement.exists()).scalar()

    def find_login(self, session: Session, email: str) -> Optional[User]:
        self.user_qs.by_email(email)
        result = session.scalars(self.user_qs.statement).one_or_none()
        return result

    def clean_unused(self, session: Session, autocommit: bool = True):
        self.user_qs.delete().unused()
        session.execute(self.user_qs.statement)

        if autocommit:
            session.commit()
