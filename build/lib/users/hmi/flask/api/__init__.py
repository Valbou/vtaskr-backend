from logging import Logger

from flask import Blueprint
from src.libs.openapi.base import openapi

logger = Logger(__name__)


users_bp = Blueprint(
    name="users_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


V1 = "/api/v1"
API_ERROR_COMPONENT = "#/components/schemas/APIError"

from .v1 import *
