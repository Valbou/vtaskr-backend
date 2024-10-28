from flask import current_app
from flask.cli import with_appcontext
from src.users.services import UsersService

from . import users_cli_bp


@users_cli_bp.cli.command("refresh_admin_rights")
@with_appcontext
def refresh_admin_rights():
    user_service = UsersService(services=current_app.dependencies)
    user_service.create_new_role
