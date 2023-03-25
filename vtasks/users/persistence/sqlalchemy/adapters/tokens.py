from typing import Optional

from sqlalchemy import and_, delete, or_, select, update
from sqlalchemy.orm import Session

from vtasks.users.models import Token
from vtasks.users.persistence.ports import AbstractTokenPort


class TokenDB(AbstractTokenPort):
    def load(self, session: Session, id: str) -> Optional[Token]:
        stmt = select(Token).where(Token.id == id)
        result = session.scalars(stmt).one_or_none()
        return result

    def get_token(self, session: Session, sha_token: str) -> Optional[Token]:
        stmt = select(Token).where(Token.sha_token == sha_token)
        result = session.scalars(stmt).one_or_none()
        return result

    def activity_update(self, session: Session, token: Token, autocommit: bool = True):
        stmt = (
            update(Token)
            .where(Token.id == token.id)
            .values(last_activity_at=token.update_last_activity())
        )
        session.execute(stmt)
        if autocommit:
            session.commit()

    def save(self, session: Session, token: Token, autocommit: bool = True):
        session.add(token)
        if autocommit:
            session.commit()

    def clean_expired(self, session: Session, autocommit: bool = True):
        stmt = delete(Token).where(
            or_(
                Token.last_activity_at < Token.expired_before(),
                and_(
                    Token.created_at < Token.expired_temp_before(),
                    Token.temp == True,  # noqa: E712
                ),
            )
        )
        session.execute(stmt)
        if autocommit:
            session.commit()

    def delete(self, session: Session, token: Token, autocommit: bool = True):
        session.delete(token)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        return session.query(select(Token).where(Token.id == id).exists()).scalar()
