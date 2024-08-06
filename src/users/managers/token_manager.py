from src.libs.dependencies import DependencyInjector
from src.users.models import Token
from src.users.persistence import TokenDBPort
from src.users.settings import APP_NAME


class TokenManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.token_db: TokenDBPort = self.services.persistence.get_repository(
            APP_NAME, "Token"
        )

    def create_token(self, session, user_id: str) -> Token:
        """Create a new token"""

        token = Token(user_id=user_id)
        self.update_token(session=session, token=token)

        return token

    def get_token(self, session, sha_token: str) -> Token | None:
        """Retrieve a token from sha string"""

        return self.token_db.get_token(session=session, sha_token=sha_token)

    def clean_expired(self, session) -> None:
        """Clean all expired tokens from persistence"""

        return self.token_db.clean_expired(session=session)

    def update_token(self, session, token: Token) -> bool:
        """Save or update token"""

        self.token_db.save(session=session, obj=token)
        return True

    def delete_token(self, session, token: Token) -> bool:
        """Delete a token from persistence"""

        self.token_db.delete(session=session, obj=token)
        return True
