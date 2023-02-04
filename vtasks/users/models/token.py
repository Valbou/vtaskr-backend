from uuid import uuid4
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from hashlib import sha256


@dataclass
class Token:
    id: str = ""
    created_at: datetime = datetime.now()
    sha_token: str = ""
    user_id: str = ""

    def __init__(
        self,
        user_id: str,
        token: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4().hex
        self.created_at = created_at or datetime.now()

        self.sha_token = token or sha256(str(uuid4()).encode()).hexdigest()
        self.user_id = user_id

    def __str__(self) -> str:
        return f"Token {self.sha_token}"

    def __repr__(self):
        return f"<Token {self.sha_token!r}>"
