from src.libs.hmi.default_mapper import filter_fields
from src.notifications.hmi.dto import ContactDTO, ContactMapperDTO
from src.notifications.models import Contact
from src.notifications.persistence import ContactDBPort
from src.notifications.services import NotificationService
from src.notifications.settings import APP_NAME
from src.ports import ObserverPort
from src.settings import LOCALE, TIMEZONE


class UsersRegisterUserObserver(ObserverPort):
    event_name: str = "users:register:user"

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        filtered_data = filter_fields(ContactDTO, event_data)
        contact = ContactMapperDTO.dto_to_model(ContactDTO(**filtered_data))
        service.add_new_contact(contact=contact)

        messages = service.build_messages(name=event_name, context=event_data)
        service.add_messages(messages=messages)
        service.notify_all()


class UsersLogin2FAUserObserver(ObserverPort):
    event_name: str = "users:login_2fa:user"

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)
        messages = service.build_messages(name=event_name, context=event_data)
        service.add_messages(messages=messages)


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
                contact: Contact | None = contact_db.load(session, id=contact_id)

                if contact:
                    contact.email = event_data.get("email", "")
                    contact.telegram = event_data.get("telegram", "")
                    contact.phone_number = event_data.get("phone_number", "")

                    contact_db.update(session, obj=contact)

                else:
                    contact = Contact(
                        id=event_data.get("tenant_id", ""),
                        first_name=event_data.get("first_name", ""),
                        last_name=event_data.get("last_name", ""),
                        timezone=event_data.get("timezone", TIMEZONE),
                        locale=event_data.get("locale", LOCALE),
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
                contact_db.delete_by_id(session, id=contact_id)
