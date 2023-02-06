from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from vtasks.users.persistence.ports import AbstractTokenPort
from vtasks.users.models import Token


class TokenDB(AbstractTokenPort):
    def load(self, session: Session, id: str) -> Token:
        stmt = select(Token).where(Token.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def get_token(self, session: Session, sha_token: str) -> Token:
        stmt = select(Token).where(Token.sha_token == sha_token)
        result = session.scalars(stmt).one_or_none()
        return result

    def activity_update(
        self, session: Session, token: Token, autocommit: bool = True
    ) -> True:
        stmt = (
            update(Token)
            .where(Token.id == token.id)
            .values(last_activity_at=token.update_last_activity())
        )
        result = session.execute(stmt)
        if autocommit:
            session.commit()
        return result

    def save(self, session: Session, token: Token, autocommit: bool = True) -> True:
        session.add(token)
        if autocommit:
            session.commit()
        return True

    def clean_expired(self, session: Session, autocommit: bool = True) -> int:
        stmt = delete(Token).where(Token.last_activity_at < Token.expired_before())
        result = session.execute(stmt)
        if autocommit:
            session.commit()
        return result

    def delete(self, session: Session, token: Token, autocommit: bool = True) -> True:
        session.delete(token)
        if autocommit:
            session.commit()
        return True

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Token).where(Token.id == id).exists()).scalar()
