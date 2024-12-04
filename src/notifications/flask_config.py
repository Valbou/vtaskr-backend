from jinja2 import FileSystemLoader

from flask import Flask
from src.notifications.events import UsersRegisterUserObserver
from src.notifications.hmi.flask.cli import notification_cli_bp
from src.notifications.persistence.sqlalchemy.adapters import ContactDB, SubscriptionDB
from src.notifications.settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    app.register_blueprint(notification_cli_bp, cli_group=APP_NAME.lower())

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
