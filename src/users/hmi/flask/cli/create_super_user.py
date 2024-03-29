from getpass import getpass

from flask import current_app
from flask.cli import with_appcontext
from src.users.hmi.dto import UserDTO
from src.users.services import UserService

from . import users_cli_bp


@users_cli_bp.cli.command("create_super_user")
@with_appcontext
def create_super_user():
    with current_app.sql.get_session() as session:
        user_service = UserService(session=session)
        user_dto = UserDTO(
            first_name=input("First name"),
            last_name=input("Last name"),
            email=input("email"),
            locale=input("Locale (default=en_GB)") or "en_GB",
            timezone=input("Timezone (default=Europe/London)"),
        )
        user, group = user_service.register(
            user_dto=user_dto, password=getpass("Password")
        )
