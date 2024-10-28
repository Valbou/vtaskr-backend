from logging import Logger

from flask import Blueprint

logger = Logger(__name__)

users_cli_bp = Blueprint(
    name="users_cli",
    import_name=__name__,
)


from .create_super_user import *
from .refresh_admin_rights import *
