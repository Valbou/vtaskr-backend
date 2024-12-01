from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

from src.libs.security.utils import get_id


@dataclass
class Event:
    tenant_id: str
    name: str
    data: dict = field(default_factory=dict)
    id: str = field(kw_only=True, default="")
    created_at: datetime | None = field(kw_only=True, default=None)

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
