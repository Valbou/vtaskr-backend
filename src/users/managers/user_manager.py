from src.libs.dependencies import DependencyInjector
from src.users.models import User
from src.users.persistence import UserDBPort
from src.users.settings import APP_NAME


class UserManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.user_db: UserDBPort = self.services.persistence.get_repository(
            APP_NAME, "User"
        )

    def create_user(
        self,
        session,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        locale: str,
        timezone: str,
    ) -> User:
        """Create a new persistent user"""

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            locale=locale,
            timezone=timezone,
        )
        user.set_password(password)
        self.user_db.save(session, user)

        return user

    def get_user(self, session, user_id: str) -> User | None:
        return self.user_db.load(session=session, id=user_id)

    def update_user(self, session, user: User) -> bool:
        """Update some fields of an user object"""

        self.user_db.save(session, obj=user)

        return True

    def delete_user(self, session, user: User) -> bool:
        """Delete an user object definitely"""

        self.user_db.delete(session=session, obj=user)

        return True

    def find_user_by_email(self, session, email: str) -> User | None:
        """Find a user object from an email"""

        return self.user_db.find_user_by_email(session, email=email)

    def clean_users(self):
        """Clean all users created an never logged in"""

        with self.services.persistence.get_session() as session:
            self.user_db.clean_unused(session)
