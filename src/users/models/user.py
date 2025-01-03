from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from babel import Locale

from src.libs.security.utils import check_password, get_id, hash_from_password
from src.libs.security.validators import PasswordChecker, get_valid_email
from src.settings import LOCALE, TIMEZONE, UNUSED_ACCOUNT_DELAY


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    timezone: str | None = None
    locale: Locale | None = None
    hash_password: str | None = None
    id: str | None = None
    created_at: datetime | None = None
    last_login_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
        self.locale = self.locale or Locale.parse(LOCALE)
        self.timezone = self.timezone or TIMEZONE
        self.set_email(self.email.lower())

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def set_email(self, email: str) -> bool:
        self.email = get_valid_email(email) or ""
        return True

    def set_password(self, password: str) -> bool:
        self._check_password_complexity(password)
        self.hash_password = hash_from_password(password)
        return True

    def check_password(self, password: str) -> bool:
        if self.hash_password:
            return check_password(self.hash_password, password)
        return False

    def _check_password_complexity(self, password: str) -> bool:
        password_checker = PasswordChecker()
        password_checker.check_complexity(password)
        return True

    def update_last_login(self) -> datetime:
        self.last_login_at = datetime.now(tz=ZoneInfo("UTC"))
        return self.last_login_at

    @classmethod
    def unused_before(cls) -> datetime:
        return datetime.now(tz=ZoneInfo("UTC")) - timedelta(days=UNUSED_ACCOUNT_DELAY)

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self):
        return f"<User {self.full_name!r}>"
