from logging import Logger

from flask import Blueprint

logger = Logger(__name__)

notification_cli_bp = Blueprint(
    name="notifications_cli",
    import_name=__name__,
)


from .send_notification import *
