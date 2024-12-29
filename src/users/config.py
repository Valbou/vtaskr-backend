from jinja2 import FileSystemLoader

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


def common_data(project_dir: str) -> dict:
    return {
        "domains": [APP_NAME.lower()],
        "loaders": [
            FileSystemLoader(f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates")
        ],
        "observers": [],
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


def setup_celery(app, project_dir: str) -> dict:
    """Must be called only if a Celery app is needed"""

    return common_data(project_dir=project_dir)


def setup_flask(app, project_dir: str) -> dict:
    """Must be called only if a Flask app is needed"""

    from flask import Flask
    from src.users.hmi.flask import users_bp, users_cli_bp

    local_app: Flask = app
    local_app.register_blueprint(users_bp)
    local_app.register_blueprint(users_cli_bp, cli_group=APP_NAME.lower())

    return common_data(project_dir=project_dir)
