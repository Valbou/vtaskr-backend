from dataclasses import dataclass
from datetime import datetime, timedelta

from pytz import utc

from src.base.config import TOKEN_TEMP_VALIDITY, TOKEN_VALIDITY
from src.libs.secutity.utils import get_2FA, get_id, get_token


@dataclass
class Token:
    user_id: str
    temp: bool = True
    temp_code: str | None = None
    sha_token: str | None = None
    id: str | None = None
    created_at: datetime | None = None
    last_activity_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(utc)
        self.last_activity_at = self.last_activity_at or self.created_at
        if not self.sha_token:
            self.sha_token = get_token()
        self.temp_code = self.temp_code or get_2FA()

    def set_token(self, token: str):
        self.sha_token = token or get_token()

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
    def expired_temp_before(cls) -> datetime:
        return datetime.now(utc) - timedelta(seconds=TOKEN_TEMP_VALIDITY)

    @classmethod
    def expired_before(cls) -> datetime:
        return datetime.now(utc) - timedelta(seconds=TOKEN_VALIDITY)
