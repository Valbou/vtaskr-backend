from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from src.libs.security.utils import get_id
from src.notifications.settings import MessageType

from .contact import Contact


@dataclass
class Subscription:
    """To receive notifications"""

    type: MessageType
    name: str
    contact_id: str
    contact: Contact
    id: str | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))
