from typing import Tuple

from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions, Resources
from src.users import Group, RequestChange, RequestType, Token, User
from src.users.events import UsersEventService
from src.users.hmi.dto import UserDTO
from src.users.persistence import RequestChangeDBPort, TokenDBPort, UserDBPort
from src.users.settings import APP_NAME

from .emails_service import EmailService


class EmailAlreadyUsedError(Exception):
    pass


class UserService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event = UsersEventService(self.services.eventbus)

        self.user_db: UserDBPort = self.services.persistence.get_repository(
            APP_NAME, "User"
        )
        self.token_db: TokenDBPort = self.services.persistence.get_repository(
            APP_NAME, "Token"
        )
        self.request_change_db: RequestChangeDBPort = (
            self.services.persistence.get_repository(APP_NAME, "RequestChange")
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
            if self.user_db.find_login(session, email=user.email):
                raise ValueError(f"User {user.email} already exists")

            self.user_db.save(session, user)

        from .group_service import GroupService

        group_service = GroupService(services=self.services)
        group = group_service.create_private_group(user_id=user.id)

        self.event.send_register_event(user=user, group=group)

        email_service = EmailService(services=self.services)
        context = email_service.get_register_context(user=user)
        message = self.services.notification.build_message(context)
        self.services.notification.add_message(message=message)
        self.services.notification.notify_all()

        return (user, group)

    def find_login(self, email: str) -> User | None:
        with self.services.persistence.get_session() as session:
            return self.user_db.find_login(session, email=email)

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
            user = self.user_db.find_login(session, email)

            if isinstance(user, User) and user.check_password(password):
                # Many tokens can be active for a unique user (it's assumed)
                user.update_last_login()
                session.commit()

                token = Token(user_id=user.id)
                self.token_db.save(session, token)

                email_service = EmailService(services=self.services)
                context = email_service.get_login_context(
                    user=user, code=token.temp_code
                )
                message = self.services.notification.build_message(context)
                self.services.notification.add_message(message=message)
                self.services.notification.notify_all()

                return token, user
            return None, None

    def get_token(self, sha_token: str, code: str) -> Token | None:
        with self.services.persistence.get_session() as session:
            token = self.token_db.get_token(session, sha_token=sha_token)
            if code and token and token.is_temp_valid() and token.validate_token(code):
                self.token_db.save(session, token)
                return token
            return None

    def logout(self, sha_token: str) -> bool:
        """Delete active token for this user only"""

        with self.services.persistence.get_session() as session:
            token = self.token_db.get_token(session, sha_token)
            if token:
                self.token_db.delete(session, token)
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

    def request_password_change(self, user: User) -> str:
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
            user_found = self.user_db.find_login(session, new_email)

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

    def _request_change(self, email: str, request_type: RequestType) -> RequestChange:
        with self.services.persistence.get_session() as session:
            self.request_change_db.clean_history(session)
            request_change = RequestChange(request_type, email=email)
            self.request_change_db.save(session, request_change)
            return request_change

    def update(self, user: User) -> None:
        """Update user"""
        with self.services.persistence.get_session() as session:
            self.user_db.update(session, user)

    def set_new_password(self, email: str, hash: str, password: str) -> bool:
        """Set the new password to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(session, email)

            if (
                request_change
                and request_change.request_type == RequestType.PASSWORD
                and request_change.check_hash(hash=hash)
            ):
                user = self.user_db.find_login(session, email)
                user.set_password(password)
                session.commit()

                return True
            return False

    def set_new_email(
        self, old_email: str, new_email: str, hash: str, code: str
    ) -> bool:
        """Set the new email to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(session, old_email)

            if (
                request_change
                and request_change.check_hash(hash=hash)
                and request_change.check_code(code)
            ):
                user = self.user_db.find_login(session, old_email)
                user.set_email(new_email)
                session.commit()

                return True
            return False

    def delete(self, user: User) -> bool:
        """
        Delete a user if he is not an admin of many groups
        Otherwise it can lead to a deadlock for members left
        """

        with self.services.persistence.get_session() as session:
            group_id = self.services.identity.all_tenants_with_access(
                session, Permissions.CREATE, user.id, Resources.ROLETYPE
            )
            if len(group_id) <= 1:
                self.user_db.delete(session, user)
                return True
            return False
