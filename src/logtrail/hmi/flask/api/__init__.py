from logging import Logger

from flask import Blueprint
from src.libs.openapi.base import openapi

logger = Logger(__name__)


logtrails_bp = Blueprint(
    name="logtrails_bp",
    import_name=__name__,
)


V1 = "/api/v1"
API_ERROR_COMPONENT = "#/components/schemas/APIError"

from .v1 import *
