from flask import current_app
from flask.cli import with_appcontext
from src.tasks.services import TasksService

from . import logger, tasks_cli_bp


@tasks_cli_bp.cli.command("todays_tasks")
@with_appcontext
def todays_tasks() -> int:
    service = TasksService(services=current_app.dependencies)
    nb_users = service.send_today_tasks_notifications()

    logger.info(f"{nb_users} users with daily tasks")
