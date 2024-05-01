from logging import Logger

from flask import Blueprint

logger = Logger(__name__)

event_cli_bp = Blueprint(
    name="events_cli",
    import_name=__name__,
)


from .clean_db import *
