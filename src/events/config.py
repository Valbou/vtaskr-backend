from src.events.persistence.sqlalchemy import EventDB

from .settings import APP_NAME


def common_data(project_dir: str) -> dict:
    return {
        "domains": [APP_NAME],
        "repositories": [
            (APP_NAME, "Event", EventDB()),
        ],
        "permissions_resources": [
            "Event",
        ],
    }


def setup_celery(app, project_dir: str) -> dict:
    """Must be called only if a Celery app is needed"""

    from src.events.jobs import schedule_tasks

    schedule_tasks(app=app)

    return common_data(project_dir=project_dir)


def setup_flask(app, project_dir: str) -> dict:
    """Must be called only if a Flask app is needed"""

    from flask import Flask
    from src.events.hmi.flask import events_bp, events_cli_bp

    local_app: Flask = app
    local_app.register_blueprint(events_bp)
    local_app.register_blueprint(events_cli_bp, cli_group=APP_NAME.lower())

    return common_data(project_dir=project_dir)
