from typing import Optional, Tuple

from sqlalchemy.orm import Session

from vtasks.users import User, Token
from vtasks.users.persistence import UserDB, TokenDB
from vtasks.users.hmi.ports import AbstractUserPort


class UserService(AbstractUserPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.user_db = UserDB()
        self.token_db = TokenDB()

    def register(self, data: dict) -> User:
        """Add a new user"""
        user = User(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
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

    def logout(self, email: str, sha_token: str) -> bool:
        """Delete active token for this user only"""
        user = self.user_db.find_login(self.session, email)
        token = self.token_db.get_token(self.session, sha_token)
        if user and token and token.user_id == user.id:
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
