from src.libs.hmi.default_mapper import filter_fields
from src.notifications.hmi.dto import ContactDTO, ContactMapperDTO
from src.notifications.services import NotificationService
from src.ports import ObserverPort


class UsersRegisterUserObserver(ObserverPort):
    subscribe_to: list[str] = ["users:register:user"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        filtered_data = filter_fields(ContactDTO, event_data)
        contact = ContactMapperDTO.dto_to_model(ContactDTO(**filtered_data))
        service.add_new_contact(contact=contact)

        messages = service.build_messages(name=event_name, context=event_data)
        service.add_messages(messages=messages)
        service.notify_all()


class UsersUpdateUserObserver(ObserverPort):
    subscribe_to: list[str] = ["users:update:user"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        filtered_data = filter_fields(ContactDTO, event_data)
        contact = ContactMapperDTO.dto_to_model(ContactDTO(**filtered_data))
        contact.id = event_data.get("user_id")
        service.update_contact(contact=contact)


class UsersDeleteUserObserver(ObserverPort):
    subscribe_to: list[str] = ["users:delete:user"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        filtered_data = filter_fields(ContactDTO, event_data)
        contact = ContactMapperDTO.dto_to_model(ContactDTO(**filtered_data))
        contact.id = event_data.get("user_id")
        service.delete_contact(contact=contact)


class UsersNotificationsObserver(ObserverPort):
    subscribe_to: list[str] = [
        "users:login_2fa:user",
        "users:invite:user",
        "users:accepted:invitation",
        "users:cancelled:invitation",
    ]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        messages = service.build_messages(name=event_name, context=event_data)
        service.add_messages(messages=messages)
        service.notify_all()
