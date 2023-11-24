from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from src.colors.models.color import Color
from src.libs.security.utils import get_id


@dataclass
class Role:
    user_id: str
    group_id: str
    roletype_id: str
    color: Color | None = None
    id: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
        self.color = self.color or Color(background="#FFFFFF", text="#000000")
