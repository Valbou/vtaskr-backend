from typing import Optional

from sqlalchemy.orm import Session

from vtasks.users import User, Token
from vtasks.users.persistence import UserDB, TokenDB


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def authenticate(self, email: str, password: str) -> Optional[str]:
        """Create a token only if user and password are ok"""
        user_db = UserDB()
        token_db = TokenDB()

        token_db.clean_expired(self.session)
        user = user_db.find_login(self.session, email)
        if isinstance(user, User) and user.check_password(password):
            # Many tokens can be active for a unique user (it's assumed)
            user.update_last_login()
            self.session.commit()
            token = Token(user_id=user.id)
            token_db.save(self.session, token)
            return token.sha_token
        return None

    def logout(self, email: str, sha_token: str) -> bool:
        """Delete active token for this user only"""
        user_db = UserDB()
        token_db = TokenDB()

        user = user_db.find_login(self.session, email)
        token = token_db.get_token(self.session, sha_token)
        if user and token and token.user_id == user.id:
            token_db.delete(self.session, token)
            return True
        return False

    def user_from_token(self, sha_token: str) -> Optional[User]:
        user_db = UserDB()
        token_db = TokenDB()

        token = token_db.get_token(self.session, sha_token)
        if token.is_valid():
            token.update_last_activity()
            self.session.commit()
            user = user_db.load(self.session, token.user_id)
            return user
        return None
