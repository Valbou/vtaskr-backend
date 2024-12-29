from jinja2 import FileSystemLoader

from src.tasks.events import UsersDeleteTenantObserver
from src.tasks.persistence.sqlalchemy import TagDB, TaskDB

from .settings import APP_NAME


def common_data(project_dir: str) -> dict:
    return {
        "domains": [APP_NAME],
        "loaders": [
            FileSystemLoader(f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates")
        ],
        "observers": [
            UsersDeleteTenantObserver(),
        ],
        "repositories": [
            (APP_NAME, "Tag", TagDB()),
            (APP_NAME, "Task", TaskDB()),
        ],
        "permissions_resources": ["Task", "Tag"],
    }


def setup_celery(app, project_dir: str) -> dict:
    """Must be called only if a Celery app is needed"""

    from src.tasks.jobs import schedule_tasks

    schedule_tasks(app=app)

    return common_data(project_dir=project_dir)


def setup_flask(app, project_dir: str) -> dict:
    """Must be called only if a Flask app is needed"""

    from flask import Flask
    from src.tasks.hmi.flask import tasks_bp, tasks_cli_bp

    local_app: Flask = app
    local_app.register_blueprint(tasks_bp)
    local_app.register_blueprint(tasks_cli_bp, cli_group=APP_NAME.lower())

    return common_data(project_dir=project_dir)
