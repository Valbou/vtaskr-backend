from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo


@dataclass
class BaseModel:
    id: str = field(kw_only=True, default="")
    created_at: datetime | None = field(kw_only=True, default=None)

    def __post_init__(self):
        self._set_id()
        self.created_at = (
            self.created_at or datetime.now(tz=ZoneInfo("UTC")).isoformat()
        )

    def _set_id(self):
        if not self.id:
            self.id = uuid4().hex
