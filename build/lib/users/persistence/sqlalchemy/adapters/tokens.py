from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Token
from src.users.persistence.ports import AbstractTokenPort
from src.users.persistence.sqlalchemy.querysets import TokenQueryset


class TokenDB(AbstractTokenPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TokenQueryset()

    def get_token(self, session: Session, sha_token: str) -> Token | None:
        self.qs.by_sha(sha_token)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def activity_update(self, session: Session, token: Token, autocommit: bool = True):
        self.qs.update().id(token.id).values(
            last_activity_at=token.update_last_activity()
        )
        session.execute(self.qs.statement)
        if autocommit:
            session.commit()

    def clean_expired(self, session: Session, autocommit: bool = True):
        self.qs.delete().expired()
        session.execute(self.qs.statement)
        if autocommit:
            session.commit()
