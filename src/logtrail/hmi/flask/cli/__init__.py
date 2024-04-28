from logging import Logger

from flask import Blueprint

logger = Logger(__name__)

logtrail_cli_bp = Blueprint(
    name="logtrails_cli",
    import_name=__name__,
)


from .clean_db import *
