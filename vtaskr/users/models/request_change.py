from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from pytz import utc

from vtaskr.base.config import REQUEST_DAYS_HISTORY, REQUEST_VALIDITY
from vtaskr.libs.secutity.utils import get_2FA, get_id, hash_str
from vtaskr.libs.secutity.validators import get_valid_email


class RequestType(Enum):
    EMAIL = "email"
    PASSWORD = "passwd"  # nosec


@dataclass
class RequestChange:
    """
    A request change is not linked to an user directly.
    The email field permit to looking for an user if needed.
    """

    id: str = ""
    created_at: datetime = datetime.now(utc)
    request_type: RequestType | None = None
    email: str = ""
    code: str = ""
    done: bool = False

    def __init__(
        self,
        request_type: RequestType,
        email: str,
        done: bool = False,
        code: str | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.request_type = request_type
        self.set_email(email.lower())
        self.code = code or get_2FA()
        self.done = done

    def _gen_base_hash_string(self) -> str:
        return f"{self.id}_{self.email}_{self.request_type.value}"

    def gen_hash(self):
        base_string = self._gen_base_hash_string()
        return hash_str(base_string)

    def check_hash(self, hash: str) -> bool:
        return self.gen_hash() == hash

    def check_code(self, code: str) -> bool:
        return self.code == code

    def mark_as_done(self):
        self.done = True

    def set_email(self, email: str) -> bool:
        try:
            self.email = get_valid_email(email or "")
            return True
        except Exception:
            return False

    def is_valid(self) -> bool:
        """
        A RequestChange is valid only if it's creation date is less older than REQUEST_VALIDITY
        """
        delta: timedelta = datetime.now(utc) - self.created_at
        return not self.done and 0 <= delta.seconds < REQUEST_VALIDITY

    @classmethod
    def history_expired_before(cls) -> datetime:
        return datetime.now(utc) - timedelta(days=REQUEST_DAYS_HISTORY)

    @classmethod
    def valid_after(cls) -> datetime:
        return datetime.now(utc) - timedelta(seconds=REQUEST_VALIDITY)
