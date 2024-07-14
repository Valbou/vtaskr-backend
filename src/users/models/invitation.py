from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.libs.security.utils import get_id, hash_str
from src.settings import INVITE_VALIDITY
from src.users.models import Group, RoleType, User


@dataclass
class Invitation:
    from_user_id: str
    to_user_email: str
    with_roletype_id: str
    in_group_id: str
    hash: str = ""
    from_user: User | None = None
    in_group: Group | None = None
    with_roletype: RoleType | None = None
    id: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
        self.hash = self.gen_hash()

    def _gen_base_hash_string(self) -> str:
        return (
            f"{self.id}_{self.from_user_id}_{self.to_user_email}"
            f"_{self.with_roletype_id}_{self.in_group_id}"
        )

    def gen_hash(self):
        return hash_str(self._gen_base_hash_string())

    def check_hash(self, hash: str) -> bool:
        return self.gen_hash() == hash

    def is_valid(self) -> bool:
        """
        An invitation is valid only if it's creation date is less older than INVITE_VALIDITY
        """
        delta: timedelta = datetime.now(tz=ZoneInfo("UTC")) - self.created_at
        return 0 <= delta.seconds < INVITE_VALIDITY

    @classmethod
    def expired_before(cls) -> datetime:
        return datetime.now(tz=ZoneInfo("UTC")) - timedelta(seconds=INVITE_VALIDITY)
