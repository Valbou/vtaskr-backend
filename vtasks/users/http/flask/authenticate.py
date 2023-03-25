from typing import Optional

from flask import Flask

from vtasks.users import User, Token
from vtasks.users.persistence import UserDB, TokenDB


class AuthService:
    def authenticate(
        self, current_app: Flask, email: str, password: str
    ) -> Optional[str]:
        """Create a token only if user and password are ok"""
        user_db = UserDB()
        token_db = TokenDB()

        with current_app.sql_service.get_session() as session:
            token_db.clean_expired(session)
            user = user_db.find_login(session, email)
            if isinstance(user, User) and user.check_password(password):
                # Many tokens can be active for a unique user (it's assumed)
                user.update_last_login()
                session.commit()
                token = Token(user_id=user.id)
                token_db.save(session, token)
                return token.sha_token
        return None

    def logout(self, current_app: Flask, email: str, sha_token: str) -> bool:
        """Delete active token for this user only"""
        user_db = UserDB()
        token_db = TokenDB()

        with current_app.sql_service.get_session() as session:
            user = user_db.find_login(session, email)
            token = token_db.get_token(session, sha_token)
            if user and token and token.user_id == user.id:
                token_db.delete(session, token)
                return True
            return False

    def user_from_token(self, current_app: Flask, sha_token: str) -> Optional[User]:
        user_db = UserDB()
        token_db = TokenDB()

        with current_app.sql_service.get_session() as session:
            token = token_db.get_token(session, sha_token)
            if token.is_valid():
                token.update_last_activity()
                session.commit()
                user = user_db.load(session, token.user_id)
                return user
        return None
