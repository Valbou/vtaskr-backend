from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from src.libs.iam.constants import Permissions, Resources
from src.libs.security.utils import get_id


@dataclass
class Right:
    """EAV like model"""

    roletype_id: str
    resource: Resources
    permissions: list[Permissions] | None = None
    id: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
        self.permissions = self.permissions or [
            Permissions.READ,
        ]
