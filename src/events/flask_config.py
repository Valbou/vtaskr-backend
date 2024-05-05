from flask import Flask
from src.events.persistence.sqlalchemy import EventDB
from src.events.settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    return {
        "domains": [APP_NAME],
        "repositories": [
            (APP_NAME, "Event", EventDB()),
        ],
    }
