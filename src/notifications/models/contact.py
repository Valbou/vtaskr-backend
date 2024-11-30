from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from babel import Locale

from src.libs.security.utils import get_id


@dataclass
class Contact:
    """
    To send notification informations

    tenant_id is used as an id.
    tenant_id may be a user id (individual user)
    or a group id (mailing list, group telegram with many readers...)
    """

    first_name: str
    last_name: str
    timezone: str | None = None
    locale: Locale | None = None
    email: str = ""
    telegram: str = ""
    phone_number: str = ""
    id: str | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))

        if isinstance(self.locale, str):
            self.locale = Locale.parse(self.locale)
