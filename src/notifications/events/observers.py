from src.notifications.models import Contact
from src.notifications.persistence import ContactDBPort
from src.notifications.settings import APP_NAME
from src.ports import ObserverPort


class UsersRegisterObserver(ObserverPort):
    event_name: str = "users:register"

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        contact = Contact(
            id=event_data.get("tenant_id", ""),
            email=event_data.get("email", ""),
            telegram=event_data.get("telegram", ""),
            phone_number=event_data.get("phone_number", ""),
        )

        contact_db: ContactDBPort = app_ctx.dependencies.persistence.get_repository(
            APP_NAME, "Contact"
        )

        with app_ctx.dependencies.persistence.get_session() as session:
            contact_db.save(session, obj=contact)
            session.commit()
