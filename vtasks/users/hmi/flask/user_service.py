from typing import Optional, Tuple

from sqlalchemy.orm import Session

from vtasks.users import User, Token, RequestChange, RequestType
from vtasks.users.persistence import UserDB, TokenDB, RequestChangeDB
from vtasks.users.hmi.ports import AbstractUserPort


class EmailAlreadyUsedError(Exception):
    pass


class UserService(AbstractUserPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.user_db = UserDB()
        self.token_db = TokenDB()
        self.request_change_db = RequestChangeDB()

    def register(self, data: dict) -> User:
        """Add a new user"""
        user = User(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
            locale=data.get("locale"),
            timezone=data.get("timezone"),
        )
        user.set_password(data.get("password", ""))
        self.user_db.save(self.session, user)
        return user

    def authenticate(
        self, email: str, password: str
    ) -> Tuple[Optional[Token], Optional[User]]:
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

    def user_from_token(self, sha_token: str) -> Optional[User]:
        """Load a user from a given token"""
        token = self.token_db.get_token(self.session, sha_token)
        if token.is_valid():
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
