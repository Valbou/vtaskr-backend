from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.notifications.models import Contact
from src.notifications.persistence.ports import ContactDBPort
from src.notifications.persistence.sqlalchemy.querysets import ContactQueryset


class ContactDB(ContactDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = ContactQueryset()

    def update(self, session: Session, contact: Contact) -> bool:
        self.qs.update().id(contact.id).values(
            email=contact.email,
            first_name=contact.first_name,
            last_name=contact.last_name,
            timezone=contact.timezone,
            locale=contact.locale,
            telegram=contact.telegram,
            phone_number=contact.phone_number,
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
        )
        session.execute(self.qs.statement)
