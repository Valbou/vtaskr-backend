from jinja2 import FileSystemLoader

from src.notifications.events import UsersRegisterUserObserver
from src.notifications.persistence.sqlalchemy.adapters import ContactDB, SubscriptionDB
from src.notifications.settings import APP_NAME


def common_data(project_dir: str) -> dict:
    return {
        "domains": [APP_NAME],
        "loaders": [
            FileSystemLoader(f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates")
        ],
        "observers": [
            UsersRegisterUserObserver(),
        ],
        "repositories": [
            (APP_NAME, "Subscription", SubscriptionDB()),
            (APP_NAME, "Contact", ContactDB()),
        ],
        "permissions_resources": ["Subscription"],
    }


def setup_celery(app, project_dir: str) -> dict:
    """Must be called only if a Celery app is needed"""

    return common_data(project_dir=project_dir)


def setup_flask(app, project_dir: str) -> dict:
    """Must be called only if a Flask app is needed"""

    from flask import Flask
    from src.notifications.hmi.flask.cli import notification_cli_bp

    local_app: Flask = app
    local_app.register_blueprint(notification_cli_bp, cli_group=APP_NAME.lower())

    return common_data(project_dir=project_dir)
