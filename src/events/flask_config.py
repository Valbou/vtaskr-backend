from flask import Flask
from src.events.hmi.flask import events_bp
from src.events.persistence.sqlalchemy import EventDB

from .settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    app.register_blueprint(events_bp)

    return {
        "domains": [APP_NAME],
        "repositories": [
            (APP_NAME, "Event", EventDB()),
        ],
        "permissions_resources": [
            "Event",
        ],
    }
