from sqlalchemy.orm import Session

from vtaskr.users.models import Token
from vtaskr.users.persistence import TokenDB


class TokenService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.token_db = TokenDB()

    def get_token(self, sha_token: str) -> Token | None:
        return self.token_db.get_token(self.session, sha_token=sha_token)
