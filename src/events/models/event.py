from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

from .base_model import BaseModel


@dataclass
class Event(BaseModel):
    tenant_id: str
    name: str
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        self.created_at = (
            self.created_at or datetime.now(tz=ZoneInfo("UTC")).isoformat()
        )
