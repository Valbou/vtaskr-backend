from uuid import uuid4
from datetime import datetime, timedelta
from pytz import utc
from typing import Optional
from dataclasses import dataclass
from hashlib import sha256
from base64 import b64encode


TOKEN_VALIDITY = 60 * 60 * 0.5  # 30 minutes
TOKEN_TEMP_VALIDITY = 60 * 3  # 3 minutes


@dataclass
class Token:
    id: str = ""
    created_at: datetime = datetime.now(utc)
    last_activity_at: datetime = datetime.now(utc)
    temp: bool = True
    temp_code: str = ""
    sha_token: str = ""
    user_id: str = ""

    def __init__(
        self,
        user_id: str,
        token: Optional[str] = None,
        temp: bool = True,
        temp_code: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_activity_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4().hex
        self.created_at = created_at or datetime.now(utc)
        self.last_activity_at = last_activity_at or self.created_at
        self.sha_token = token or self._gen_token()
        self.user_id = user_id
        self.temp = temp
        self.temp_code = temp_code or self._gen_temp_code()

    def _gen_token(self):
        return sha256(str(uuid4()).encode()).hexdigest()

    def _gen_temp_code(self, length: int = 6):
        """
        Generate an alphanumeric case sensitive code.
        Hard to brute-force in few minutes with API response time
        """
        return b64encode(uuid4().hex.encode())[:length].decode()

    def is_temp_valid(self) -> bool:
        """
        A Token is temp valid only if is temp and less older than TOKEN_TEMP_VALIDITY
        """
        delta: timedelta = datetime.now(utc) - self.created_at
        return self.temp and 0 <= delta.seconds < TOKEN_TEMP_VALIDITY

    def is_valid(self) -> bool:
        """
        A Token is valid only if it's last activity is under TOKEN_VALIDITY from now
        and if is not temp
        """
        delta: timedelta = datetime.now(utc) - self.last_activity_at
        return not self.temp and 0 <= delta.seconds < TOKEN_VALIDITY

    def validate_token(self, code) -> bool:
        """Method to convert a temp token to a valid token"""
        if self.temp_code == code:
            self.temp = False
            self.update_last_activity()
        return not self.temp

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
