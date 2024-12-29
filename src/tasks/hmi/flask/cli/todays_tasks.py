from flask import current_app
from flask.cli import with_appcontext
from src.tasks.services import TasksService

from . import tasks_cli_bp


@tasks_cli_bp.cli.command("todays_tasks")
@with_appcontext
def todays_tasks():
    service = TasksService(services=current_app.dependencies)
    service.send_today_tasks_notifications()
