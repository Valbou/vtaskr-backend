from src.notifications.models import Contact
from src.notifications.persistence import ContactDBPort
from src.notifications.settings import APP_NAME
from src.ports import ObserverPort


class UsersRegisterUserObserver(ObserverPort):
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


class UsersUpdateUserObserver(ObserverPort):
    event_name: str = "users:update:user"

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        contact_id = event_data.get("tenant_id")
        if contact_id:
            contact_db: ContactDBPort = app_ctx.dependencies.persistence.get_repository(
                APP_NAME, "Contact"
            )
            with app_ctx.dependencies.persistence.get_session() as session:
                contact: Contact = contact_db.load(session, id=contact_id)

                if contact:
                    contact.email = event_data.get("email", "")
                    contact.telegram = event_data.get("telegram", "")
                    contact.phone_number = event_data.get("phone_number", "")

                    contact_db.update(session, obj=contact)

                else:
                    contact = Contact(
                        id=event_data.get("tenant_id", ""),
                        email=event_data.get("email", ""),
                        telegram=event_data.get("telegram", ""),
                        phone_number=event_data.get("phone_number", ""),
                    )
                    contact_db.save(session, obj=contact)


class UsersDeleteUserObserver(ObserverPort):
    event_name: str = "users:delete:user"

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        contact_id = event_data.get("tenant_id")
        if contact_id:
            contact_db: ContactDBPort = app_ctx.dependencies.persistence.get_repository(
                APP_NAME, "Contact"
            )
            with app_ctx.dependencies.persistence.get_session() as session:
                contact_db.delete(session, id=contact_id)
