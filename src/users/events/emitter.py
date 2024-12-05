from src.ports import EventBusPort
from src.users.models import Group, Invitation, RequestChange, RoleType, Token, User


class UsersEventManager:
    def send_register_event(
        self, session: EventBusPort, user: User, group: Group
    ) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:register:user",
            event_data={
                "targets": [user.id],
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

    def send_login_2fa_event(
        self, session: EventBusPort, user: User, token: Token
    ) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:login_2fa:user",
            event_data={
                "targets": [user.id],
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "code": token.temp_code,
                "valid_until": token.get_validity_limit().isoformat(),
            },
        )

    def send_email_change_event(
        self,
        session: EventBusPort,
        user: User,
        new_email: str,
        request_change: RequestChange,
    ) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:change_email:user",
            event_data={
                "targets": [user.id],
                "email": user.email,
                "new_email": new_email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hash": request_change.gen_hash(),
                "code": request_change.code,
                "valid_until": request_change.get_validity_limit().isoformat(),
            },
        )

    def send_password_change_event(
        self, session: EventBusPort, user: User, request_change: RequestChange
    ) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:change_password:user",
            event_data={
                "targets": [user.id],
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hash": request_change.gen_hash(),
                "valid_until": request_change.get_validity_limit().isoformat(),
            },
        )

    def send_update_user_event(self, session: EventBusPort, user: User) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:update:user",
            event_data={
                "targets": [user.id],
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "timezone": user.timezone,
                "locale": str(user.locale),
                "created_at": user.created_at.isoformat(),
            },
        )

    def send_delete_user_event(self, session: EventBusPort, user: User) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:delete:user",
            event_data={
                "targets": [user.id],
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "timezone": user.timezone,
                "locale": str(user.locale),
                "created_at": user.created_at.isoformat(),
            },
        )

    def send_invitation_event(
        self,
        session: EventBusPort,
        user: User,
        group: Group,
        roletype: RoleType,
        invitation: Invitation,
    ) -> dict:
        session.emit(
            tenant_id=user.id,
            event_name="users:invite:user",
            event_data={
                "targets": [user.id],
                "from_name": f"{user.first_name} {user.last_name}",
                "timezone": user.timezone,
                "locale": str(user.locale),
                "group_name": group.name,
                "role_name": roletype.name,
                "invited_email": invitation.to_user_email,
                "hash": invitation.gen_hash(),
                "valid_until": invitation.get_validity_limit().isoformat(),
            },
        )

    def send_accepted_invitation_event(
        self,
        session: EventBusPort,
        to_user: User,
        group: Group,
        roletype: RoleType,
        from_user: User,
    ) -> dict:
        session.emit(
            tenant_id=from_user.id,
            event_name="users:accepted:invitation",
            event_data={
                "targets": [from_user.id],
                "user_id": from_user.id,
                "to_name": f"{to_user.first_name} {to_user.last_name}",
                "from_name": f"{from_user.first_name} {from_user.last_name}",
                "email": from_user.email,
                "timezone": from_user.timezone,
                "locale": str(from_user.locale),
                "group_name": group.name,
                "role_name": roletype.name,
            },
        )

    def send_cancelled_invitation_event(
        self,
        session: EventBusPort,
        from_user: User,
        group: Group,
    ) -> dict:
        session.emit(
            tenant_id=from_user.id,
            event_name="users:cancelled:invitation",
            event_data={
                "targets": [from_user.id],
                "user_id": from_user.id,
                "from_name": f"{from_user.first_name} {from_user.last_name}",
                "email": from_user.email,
                "timezone": from_user.timezone,
                "locale": str(from_user.locale),
                "group_name": group.name,
            },
        )
