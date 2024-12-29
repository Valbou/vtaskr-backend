from logging import Logger

from flask import Blueprint

logger = Logger(__name__)

tasks_cli_bp = Blueprint(
    name="tasks_cli",
    import_name=__name__,
)


from .todays_tasks import *
