from jinja2 import FileSystemLoader

from flask import Flask
from src.users.hmi.flask import users_bp
from src.users.persistence.sqlalchemy import (
    GroupDB,
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
        ],
        "permissions_resources": ["Group", "Role", "RoleType"],
    }
