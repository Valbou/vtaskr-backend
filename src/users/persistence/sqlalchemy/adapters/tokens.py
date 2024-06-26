from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Token
from src.users.persistence.ports import TokenDBPort
from src.users.persistence.sqlalchemy.querysets import TokenQueryset


class TokenDB(TokenDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TokenQueryset()

    def get_token(self, session: Session, sha_token: str) -> Token | None:
        self.qs.select().by_sha(sha_token)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def activity_update(self, session: Session, token: Token):
        self.qs.update().id(token.id).values(
            last_activity_at=token.update_last_activity()
        )
        session.execute(self.qs.statement)

    def clean_expired(self, session: Session):
        self.qs.delete().expired()
        session.execute(self.qs.statement)
