from jinja2 import FileSystemLoader

from flask import Flask
from src.users.hmi.flask import users_bp, users_cli_bp
from src.users.persistence.sqlalchemy import (
    GroupDB,
    InvitationDB,
    RequestChangeDB,
    RightDB,
    RoleDB,
    RoleTypeDB,
    TokenDB,
    UserDB,
)

from .settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    app.register_blueprint(users_bp)
    app.register_blueprint(users_cli_bp, cli_group=APP_NAME.lower())

    return {
        "domains": [APP_NAME.lower()],
        "loaders": [
            FileSystemLoader(
                f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates"
            )
        ],
        "repositories": [
            (APP_NAME, "User", UserDB()),
            (APP_NAME, "Group", GroupDB()),
            (APP_NAME, "Right", RightDB()),
            (APP_NAME, "Role", RoleDB()),
            (APP_NAME, "RoleType", RoleTypeDB()),
            (APP_NAME, "RequestChange", RequestChangeDB()),
            (APP_NAME, "Token", TokenDB()),
            (APP_NAME, "Invitation", InvitationDB()),
        ],
        "permissions_resources": ["Group", "Role", "RoleType"],
    }
