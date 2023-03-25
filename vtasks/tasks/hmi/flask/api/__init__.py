from logging import Logger

from flask import Blueprint


logger = Logger(__name__)


tasks_bp = Blueprint(
    name="tasks_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


V1 = "/api/v1"


from .v1.tasks import *
