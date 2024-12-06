from logging import getLogger

from src.libs.hmi.default_mapper import filter_fields
from src.notifications.hmi.dto import ContactDTO, ContactMapperDTO
from src.notifications.services import NotificationService
from src.ports import ObserverPort

logger = getLogger(__name__)


class UsersRegisterUserObserver(ObserverPort):
    subscribe_to: list[str] = ["users:register:user"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        user_id = event_data["user_id"]
        filtered_data = filter_fields(ContactDTO, event_data)
        contact = ContactMapperDTO.dto_to_model(ContactDTO(**filtered_data))
        service.add_new_contact(contact=contact, contact_id=user_id)

        try:
            messages = service.build_messages(name=event_name, context=event_data)
            service.add_messages(messages=messages)
            service.notify_all()
        except Exception as e:
            logger.error(f"{e}")


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
        service.delete_contact(contact_id=event_data.get("user_id"))


class UsersChangeEmailObserver(ObserverPort):
    subscribe_to: list[str] = ["users:change_email:user"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)
        messages = []

        # Old email message with code
        old_data = {
            "targets": event_data["targets"],
            "first_name": event_data["first_name"],
            "last_name": event_data["last_name"],
            "code": event_data["code"],
            "valid_until": event_data["valid_until"],
        }
        messages += service.build_messages(
            name="users:change_email_old:user", context=old_data
        )

        # New email message with hash
        user_id = event_data["user_id"]
        contact = ContactMapperDTO.dto_to_model(
            ContactDTO(
                first_name=event_data["first_name"],
                last_name=event_data["last_name"],
                email=event_data["new_email"],
            )
        )
        service.add_new_contact(contact=contact, contact_id=user_id)
        new_data = {
            "targets": [contact.id],
            "first_name": event_data["first_name"],
            "last_name": event_data["last_name"],
            "hash": event_data["hash"],
            "new_email": event_data["new_email"],
            "valid_until": event_data["valid_until"],
        }
        messages += service.build_messages(
            name="users:change_email_new:user", context=new_data
        )

        try:
            # Send both messages and clean new temp contact
            service.add_messages(messages=messages)
            service.notify_all()
        except Exception as e:
            logger.error(f"{e}")

        service.delete_contact(contact_id=contact.id)


class UsersNotificationsObserver(ObserverPort):
    subscribe_to: list[str] = [
        "users:login_2fa:user",
        "users:change_password:user",
        "users:accepted:invitation",
    ]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        try:
            messages = service.build_messages(name=event_name, context=event_data)
            service.add_messages(messages=messages)
            service.notify_all()
        except Exception as e:
            logger.error(f"{e}")


class UsersInviteUserObserver(ObserverPort):
    subscribe_to = ["users:invite:user", "users:cancelled:invitation"]

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        service = NotificationService(services=app_ctx.dependencies)

        contact = ContactMapperDTO.dto_to_model(
            ContactDTO(
                first_name="unknown",
                last_name="unknown",
                email=event_data["invited_email"],
                timezone=event_data["timezone"],
                locale=event_data["locale"],
            )
        )
        service.add_new_contact(contact=contact, contact_id=None)

        new_data = {
            "targets": [contact.id],
            "group_name": event_data["group_name"],
            "role_name": event_data.get("role_name"),
            "from_name": event_data["from_name"],
            "hash": event_data.get("hash"),
            "valid_until": event_data.get("valid_until"),
        }

        try:
            messages = service.build_messages(name=event_name, context=new_data)
            service.add_messages(messages=messages)
            service.notify_all()
        except Exception as e:
            logger.error(f"{e}")

        service.delete_contact(contact_id=contact.id)
