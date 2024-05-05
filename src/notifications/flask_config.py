from jinja2 import FileSystemLoader

from flask import Flask
from src.notifications.persistence.sqlalchemy.adapters import (
    ContactDB,
    SubscriptionDB,
    TemplateDB,
)
from src.notifications.settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    return {
        "domains": [APP_NAME],
        "loaders": [
            FileSystemLoader(
                f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates"
            )
        ],
        "repositories": [
            (APP_NAME, "Subscription", SubscriptionDB()),
            (APP_NAME, "Template", TemplateDB()),
            (APP_NAME, "Contact", ContactDB()),
        ],
        "permissions_resources": ["Subscription"],
    }
