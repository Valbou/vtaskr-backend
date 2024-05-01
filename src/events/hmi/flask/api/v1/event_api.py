from flask import current_app
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import list_dto_to_dict, list_models_to_list_dto
from src.events.hmi.dto import EventDTOMapperDTO
from src.events.services import EventService

from .. import V1, events_bp


@events_bp.route(f"{V1}/events/events", methods=["GET"])
def get_all_events():
    """Get all events"""

    event_service = EventService(current_app.dependencies)
    events = event_service.get_all()
    events_dto = list_models_to_list_dto(EventDTOMapperDTO, events)

    return ResponseAPI.get_response(list_dto_to_dict(events_dto), 200)


@events_bp.route(f"{V1}/events/events/<string:tenant_id>", methods=["GET"])
def get_events(tenant_id: str):
    """Get all events of a tenant_id"""

    event_service = EventService(current_app.dependencies)
    events = event_service.get_all_from_tenant_id(tenant_id=tenant_id)
    events_dto = list_models_to_list_dto(EventDTOMapperDTO, events)

    return ResponseAPI.get_response(list_dto_to_dict(events_dto), 200)
