from src.ports import EventBusPort
from src.users.models import Group, User


class UsersEventService:
    def __init__(self, eventbus: EventBusPort):
        self.eventbus = eventbus

    def send_register_event(self, user: User, group: Group) -> dict:
        self.eventbus.emit(
            tenant_id=user.id,
            event_name="users:register",
            event_data={
                "tenant_id": user.id,
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "timezone": user.timezone,
                "locale": str(user.locale),
                "created_at": user.created_at.isoformat(),
                "group_id": group.id,
                "group_name": group.name,
            },
        )

    def send_update_user_event(self, user: User) -> dict:
        self.eventbus.emit(
            tenant_id=user.id,
            event_name="users:update:user",
            event_data={
                "tenant_id": user.id,
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "timezone": user.timezone,
                "locale": str(user.locale),
                "created_at": user.created_at.isoformat(),
            },
        )

    def send_delete_user_event(self, user: User) -> dict:
        self.eventbus.emit(
            tenant_id=user.id,
            event_name="users:delete:user",
            event_data={
                "tenant_id": user.id,
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "timezone": user.timezone,
                "locale": str(user.locale),
                "created_at": user.created_at.isoformat(),
            },
        )
