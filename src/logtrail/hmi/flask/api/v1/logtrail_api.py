from flask import current_app
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import list_dto_to_dict, list_models_to_list_dto
from src.logtrail.hmi.dto import LogTrailDTOMapperDTO
from src.logtrail.services import LogTrailService

from .. import V1, logtrails_bp


@logtrails_bp.route(f"{V1}/logtrails/logtrails", methods=["GET"])
def get_all_logtrails():
    """Get all logtrails"""

    logtrail_service = LogTrailService(current_app.dependencies)
    logtrails = logtrail_service.get_all()
    logtrails_dto = list_models_to_list_dto(LogTrailDTOMapperDTO, logtrails)

    return ResponseAPI.get_response(list_dto_to_dict(logtrails_dto), 200)


@logtrails_bp.route(f"{V1}/logtrails/logtrails/<string:tenant_id>", methods=["GET"])
def get_logtrails(tenant_id: str):
    """Get all logtrails of a tenant_id"""

    logtrail_service = LogTrailService(current_app.dependencies)
    logtrails = logtrail_service.get_all_from_tenant_id(tenant_id=tenant_id)
    logtrails_dto = list_models_to_list_dto(LogTrailDTOMapperDTO, logtrails)

    return ResponseAPI.get_response(list_dto_to_dict(logtrails_dto), 200)
