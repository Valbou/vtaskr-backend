from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.users.models import Token
from vtaskr.users.persistence.ports import AbstractTokenPort
from vtaskr.users.persistence.sqlalchemy.querysets import TokenQueryset


class TokenDB(AbstractTokenPort):
    def __init__(self) -> None:
        super().__init__()
        self.token_qs = TokenQueryset()

    def load(self, session: Session, id: str) -> Optional[Token]:
        self.token_qs.id(id)
        result = session.scalars(self.token_qs.statement).one_or_none()
        return result

    def get_token(self, session: Session, sha_token: str) -> Optional[Token]:
        self.token_qs.by_sha(sha_token)
        result = session.scalars(self.token_qs.statement).one_or_none()
        return result

    def activity_update(self, session: Session, token: Token, autocommit: bool = True):
        self.token_qs.update().id(token.id).values(
            last_activity_at=token.update_last_activity()
        )
        session.execute(self.token_qs.statement)
        if autocommit:
            session.commit()

    def save(self, session: Session, token: Token, autocommit: bool = True):
        session.add(token)
        if autocommit:
            session.commit()

    def clean_expired(self, session: Session, autocommit: bool = True):
        self.token_qs.delete().expired()
        session.execute(self.token_qs.statement)
        if autocommit:
            session.commit()

    def delete(self, session: Session, token: Token, autocommit: bool = True):
        session.delete(token)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.token_qs.select().id(id)
        return session.query(self.token_qs.statement.exists()).scalar()
