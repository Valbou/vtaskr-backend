from uuid import uuid4
from datetime import datetime, timedelta
from pytz import utc
from typing import Optional
from dataclasses import dataclass
from hashlib import sha256


TOKEN_VALIDITY = 60 * 60 * 0.5  # 30 minutes


@dataclass
class Token:
    id: str = ""
    created_at: datetime = datetime.now(utc)
    last_activity_at: datetime = datetime.now(utc)
    sha_token: str = ""
    user_id: str = ""

    def __init__(
        self,
        user_id: str,
        token: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_activity_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4().hex
        self.created_at = created_at or datetime.now(utc)
        self.last_activity_at = last_activity_at or self.created_at
        self.sha_token = token or sha256(str(uuid4()).encode()).hexdigest()
        self.user_id = user_id

    def is_valid(self) -> bool:
        """A Token is valid only if it's last activity is under TOKEN_VALIDITY from now"""
        delta = datetime.now(utc) - self.last_activity_at
        if 0 <= delta.seconds < TOKEN_VALIDITY:
            return True
        return False

    def update_last_activity(self) -> datetime:
        """Token validity is automaticaly extended"""
        self.last_activity_at = datetime.now(utc)
        return self.last_activity_at

    def __str__(self) -> str:
        return f"Token {self.sha_token}"

    def __repr__(self):
        return f"<Token {self.sha_token!r}>"

    @classmethod
    def expired_before(cls) -> datetime:
        return datetime.now(utc) - timedelta(seconds=TOKEN_VALIDITY)
