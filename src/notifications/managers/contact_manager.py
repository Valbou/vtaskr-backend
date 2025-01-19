from src.libs.dependencies import DependencyInjector
from src.notifications.models import Contact
from src.notifications.persistence import ContactDBPort
from src.notifications.settings import APP_NAME


class ContactManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.contact_db: ContactDBPort = self.services.persistence.get_repository(
            APP_NAME, "Contact"
        )

    def get_by_id(self, session, contact_id: str) -> Contact | None:
        return self.contact_db.load(session=session, id=contact_id)

    def get_by_email(self, session, email: str) -> Contact | None:
        return self.contact_db.load_by_email(session=session, email=email)

    def create(self, session, contact: Contact) -> Contact:
        return self.contact_db.save(session=session, obj=contact)

    def update(self, session, contact: Contact) -> Contact:
        return self.contact_db.update(session=session, obj=contact)

    def delete_by_id(self, session, contact_id: str) -> None:
        self.contact_db.delete_by_id(session=session, id=contact_id)

    def delete(self, session, contact: Contact) -> None:
        self.contact_db.delete(session=session, obj=contact)
