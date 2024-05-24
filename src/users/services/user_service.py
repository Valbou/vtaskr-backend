from typing import Tuple

from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.users.events import UsersEventService
from src.users.hmi.dto import UserDTO
from src.users.models import (
    Group,
    RequestChange,
    RequestType,
    Right,
    Role,
    RoleType,
    Token,
    User,
)
from src.users.persistence import (
    GroupDBPort,
    RequestChangeDBPort,
    RightDBPort,
    RoleDBPort,
    RoleTypeDBPort,
    TokenDBPort,
    UserDBPort,
)
from src.users.settings import APP_NAME

from .emails_service import EmailService


class EmailAlreadyUsedError(Exception):
    pass


class UserService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event = UsersEventService(self.services.eventbus)
        self._define_repositories()

    def _define_repositories(self):
        self.user_db: UserDBPort = self.services.persistence.get_repository(
            APP_NAME, "User"
        )
        self.group_db: GroupDBPort = self.services.persistence.get_repository(
            APP_NAME, "Group"
        )
        self.role_db: RoleDBPort = self.services.persistence.get_repository(
            APP_NAME, "Role"
        )
        self.roletype_db: RoleTypeDBPort = self.services.persistence.get_repository(
            APP_NAME, "RoleType"
        )
        self.right_db: RightDBPort = self.services.persistence.get_repository(
            APP_NAME, "Right"
        )
        self.token_db: TokenDBPort = self.services.persistence.get_repository(
            APP_NAME, "Token"
        )
        self.request_change_db: RequestChangeDBPort = (
            self.services.persistence.get_repository(APP_NAME, "RequestChange")
        )

    def _create_admin_rights(self, roletype_id: str) -> int:
        """Give all rights on all resources for the given roletype (Admin)"""

        with self.services.persistence.get_session() as session:
            num_rights = len(
                [
                    self.right_db.save(
                        session,
                        Right(
                            roletype_id=roletype_id,
                            resource=res,
                            permissions=[perm for perm in Permissions],
                        ),
                    )
                    for res in self.services.identity.get_resources()
                ]
            )

            # bulk insert
            session.commit()

        return num_rights

    def _get_default_admin(self) -> RoleType:
        """Looking for a default roletype named: Admin"""

        with self.services.persistence.get_session() as session:
            admin_roletype = RoleType(name="Admin", group_id=None)
            roletype, created = self.roletype_db.get_or_create(
                session=session, roletype=admin_roletype
            )
            session.commit()

            if created:
                self._create_admin_rights(roletype.id)

            return roletype

    def _request_change(self, email: str, request_type: RequestType) -> RequestChange:
        with self.services.persistence.get_session() as session:
            self.request_change_db.clean_history(session)
            request_change = RequestChange(request_type, email=email)
            self.request_change_db.save(session, request_change)
            session.commit()

            return request_change

    def add_role(self, user_id: str, group_id: str, roletype_id: str) -> Role:
        """
        Add a role for internal usage in other services only
        (example: admin access to a new group or unittesting)

        For an external request, use create_role() instead, with permission controls
        """

        role = Role(
            user_id=user_id,
            group_id=group_id,
            roletype_id=roletype_id,
        )

        with self.services.persistence.get_session() as session:
            self.role_db.save(session, role)
            session.commit()

        return role

    def find_user_by_email(self, email: str) -> User | None:
        with self.services.persistence.get_session() as session:
            return self.user_db.find_user_by_email(session, email=email)

    def create_group(self, user_id: str, group_name: str) -> Group:
        """Create a new user group"""

        with self.services.persistence.get_session() as session:
            group = Group(name=group_name)
            self.group_db.save(session, group)
            session.commit()

        roletype = self._get_default_admin()
        self.add_role(user_id=user_id, group_id=group.id, roletype_id=roletype.id)

        return group

    def create_private_group(self, user_id: str) -> Group:
        """Create a default mandatory group to use this app"""

        return self.create_group(user_id=user_id, group_name="Private")

    def get_all_groups(
        self,
        user_id: str,
        qs_filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        """Return all user associated groups"""

        with self.services.persistence.get_session() as session:
            return self.group_db.get_all_user_groups(
                session, user_id=user_id, filters=qs_filters
            )

    def register(self, user_dto: UserDTO, password: str) -> tuple[User, Group]:
        """Add a new user and his group with admin role"""

        user = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            locale=user_dto.locale,
            timezone=user_dto.timezone,
        )
        user.set_password(password)

        with self.services.persistence.get_session() as session:
            if self.user_db.find_user_by_email(session, email=user.email):
                raise ValueError(f"User {user.email} already exists")

            self.user_db.save(session, user)
            session.commit()

        group = self.create_private_group(user_id=user.id)

        self.event.send_register_event(user=user, group=group)

        email_service = EmailService(services=self.services)
        context = email_service.get_register_context(user=user)
        message = self.services.notification.build_message(context)
        self.services.notification.add_message(message=message)
        self.services.notification.notify_all()

        return (user, group)

    def clean_unused_accounts(self):
        """Clean all account whithout last_login_at"""
        with self.services.persistence.get_session() as session:
            self.user_db.clean_unused(session)

    def authenticate(
        self, email: str, password: str
    ) -> Tuple[Token | None, User | None]:
        """Create a token only if user and password are ok"""

        with self.services.persistence.get_session() as session:
            self.token_db.clean_expired(session)
            session.commit()

            user = self.user_db.find_user_by_email(session, email)

            if isinstance(user, User) and user.check_password(password):
                # Many tokens can be active for a unique user (it's assumed)
                user.update_last_login()

                token = Token(user_id=user.id)
                self.token_db.save(session, token)
                session.commit()

                email_service = EmailService(services=self.services)
                context = email_service.get_login_context(
                    user=user, code=token.temp_code
                )
                message = self.services.notification.build_message(context)
                self.services.notification.add_message(message=message)
                self.services.notification.notify_all()

                return token, user
            return None, None

    def get_temp_token(self, sha_token: str, code: str) -> Token | None:
        with self.services.persistence.get_session() as session:
            token = self.token_db.get_token(session, sha_token=sha_token)

            if code and token and token.is_temp_valid() and token.validate_token(code):
                self.token_db.save(session, token)
                session.commit()
                return token
            return None

    def logout(self, sha_token: str) -> bool:
        """Delete active token for this user only"""

        with self.services.persistence.get_session() as session:
            token = self.token_db.get_token(session, sha_token)
            if token:
                self.token_db.delete(session, token)
                session.commit()
                return True
            return False

    def user_from_token(self, sha_token: str) -> User | None:
        """Load a user from a given token"""

        with self.services.persistence.get_session() as session:
            token = self.token_db.get_token(session, sha_token)

            if token and token.is_valid():
                token.update_last_activity()

                user = self.user_db.load(session, token.user_id)
                return user
            return None

    def request_password_change(self, user: User) -> None:
        """Create a request to change the user password"""

        request_change = self._request_change(user.email, RequestType.PASSWORD)
        request_hash = request_change.gen_hash()

        email_service = EmailService(services=self.services)
        context = email_service.get_password_change_context(
            user=user, sec_hash=request_hash
        )
        message = self.services.notification.build_message(context)
        self.services.notification.add_message(message=message)
        self.services.notification.notify_all()

    def request_email_change(self, user: User, new_email: str) -> None:
        """Generate process to change email"""

        request_change = self._request_change(user.email, RequestType.EMAIL)

        with self.services.persistence.get_session() as session:
            user_found = self.user_db.find_user_by_email(session, new_email)

        if user_found:
            raise EmailAlreadyUsedError()

        email_service = EmailService(services=self.services)

        context_old_email = email_service.get_email_change_old_context(
            user=user,
            request_change=request_change,
        )
        message_old_email = self.services.notification.build_message(context_old_email)
        self.services.notification.add_message(message=message_old_email)

        context_new_email = email_service.get_email_change_new_context(
            user=user, new_email=new_email, sec_hash=request_change.gen_hash()
        )
        message_new_email = self.services.notification.build_message(context_new_email)
        self.services.notification.add_message(message=message_new_email)

        self.services.notification.notify_all()

    def update_user(self, user: User) -> None:
        """Update user"""
        with self.services.persistence.get_session() as session:
            self.user_db.update(session, user)
            session.commit()
            self.event.send_update_user_event(user=user)

    def set_new_password(self, email: str, hash: str, password: str) -> bool:
        """Set the new password to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, email, RequestType.PASSWORD
            )

            if request_change and request_change.check_hash(hash=hash):
                user = self.user_db.find_user_by_email(session, email)
                user.set_password(password)
                self.user_db.save(session, user)
                session.commit()

                return True
            return False

    def set_new_email(
        self, old_email: str, new_email: str, hash: str, code: str
    ) -> bool:
        """Set the new email to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, old_email, RequestType.EMAIL
            )

            if (
                request_change
                and request_change.check_hash(hash=hash)
                and request_change.check_code(code)
            ):
                user = self.user_db.find_user_by_email(session, old_email)
                user.set_email(new_email)
                self.user_db.save(session, user)
                session.commit()

                self.event.send_update_user_event(user=user)

                return True
            return False

    def delete_user(self, user: User) -> bool:
        """
        Delete a user if he is not an admin of many groups
        Otherwise it can lead to a deadlock for members left
        """

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.CREATE, user.id, "RoleType"
            )
            if len(group_ids) <= 1:
                self.user_db.delete(session, user)
                session.commit()

                email_service = EmailService(services=self.services)
                context = email_service.get_delete_context(user=user)
                message = self.services.notification.build_message(context)
                self.services.notification.add_message(message=message)
                self.services.notification.notify_all()

                self.event.send_delete_user_event(user=user)

                return True
            return False
