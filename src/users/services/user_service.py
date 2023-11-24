from typing import Tuple

from sqlalchemy.orm import Session

from src.libs.iam.constants import Permissions, Resources
from src.users import RequestChange, RequestType, Token, User
from src.users.hmi.dto import UserDTO
from src.users.persistence import RequestChangeDB, TokenDB, UserDB
from src.users.services import PermissionControl


class EmailAlreadyUsedError(Exception):
    pass


class UserService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.user_db = UserDB()
        self.token_db = TokenDB()
        self.request_change_db = RequestChangeDB()
        self.control = PermissionControl(session=self.session)

    def register(self, user_dto: UserDTO, password: str) -> User:
        """Add a new user and his group with admin role"""
        user = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            locale=user_dto.locale,
            timezone=user_dto.timezone,
        )
        user.set_password(password)

        if self.user_db.find_login(self.session, email=user.email):
            raise ValueError(f"User {user.email} already exists")

        self.user_db.save(self.session, user)

        from .group_service import GroupService

        group_service = GroupService(self.session)
        group = group_service.create_private_group(user_id=user.id)

        return (user, group)

    def find_login(self, email: str) -> User | None:
        return self.user_db.find_login(self.session, email=email)

    def clean_unused_accounts(self):
        """Clean all account whithout last_login_at"""

        self.user_db.clean_unused(self.session)

    def authenticate(
        self, email: str, password: str
    ) -> Tuple[Token | None, User | None]:
        """Create a token only if user and password are ok"""

        self.token_db.clean_expired(self.session)
        user = self.user_db.find_login(self.session, email)

        if isinstance(user, User) and user.check_password(password):
            # Many tokens can be active for a unique user (it's assumed)
            user.update_last_login()
            self.session.commit()
            token = Token(user_id=user.id)
            self.token_db.save(self.session, token)
            return token, user
        return None, None

    def logout(self, sha_token: str) -> bool:
        """Delete active token for this user only"""

        token = self.token_db.get_token(self.session, sha_token)
        if token:
            self.token_db.delete(self.session, token)
            return True
        return False

    def user_from_token(self, sha_token: str) -> User | None:
        """Load a user from a given token"""

        token = self.token_db.get_token(self.session, sha_token)
        if token and token.is_valid():
            token.update_last_activity()
            self.session.commit()
            user = self.user_db.load(self.session, token.user_id)
            return user
        return None

    def request_password_change(self, user: User) -> str:
        """Create a request to change the user password"""

        request_change = self._request_change(user.email, RequestType.PASSWORD)
        return request_change.gen_hash()

    def request_email_change(self, user: User, new_email: str) -> Tuple[str, str]:
        """Generate process to change email"""

        request_change = self._request_change(user.email, RequestType.EMAIL)
        user = self.user_db.find_login(self.session, new_email)
        if user:
            raise EmailAlreadyUsedError()
        return (request_change.gen_hash(), request_change.code)

    def _request_change(self, email: str, request_type: RequestType) -> RequestChange:
        self.request_change_db.clean_history(self.session)
        request_change = RequestChange(request_type, email=email)
        self.request_change_db.save(self.session, request_change)
        return request_change

    def update(self, user: User) -> None:
        """Update user"""
        self.user_db.update(self.session, user)

    def set_new_password(self, email: str, hash: str, password: str) -> bool:
        """Set the new password to user if request is ok"""

        request_change = self.request_change_db.find_request(self.session, email)

        if (
            request_change
            and request_change.request_type == RequestType.PASSWORD
            and request_change.check_hash(hash=hash)
        ):
            user = self.user_db.find_login(self.session, email)
            user.set_password(password)
            self.session.commit()
            return True

        return False

    def set_new_email(
        self, old_email: str, new_email: str, hash: str, code: str
    ) -> bool:
        """Set the new email to user if request is ok"""

        request_change = self.request_change_db.find_request(self.session, old_email)

        if (
            request_change
            and request_change.check_hash(hash=hash)
            and request_change.check_code(code)
        ):
            user = self.user_db.find_login(self.session, old_email)
            user.set_email(new_email)
            self.session.commit()
            return True

        return False

    def delete(self, user: User) -> bool:
        """
        Delete a user if he is not an admin of many groups
        Otherwise it can lead to a deadlock for members left
        """

        group_id = self.control.all_tenants_with_access(
            Permissions.CREATE, user.id, Resources.ROLETYPE
        )
        if len(group_id) <= 1:
            self.user_db.delete(self.session, user)
            return True
        return False
