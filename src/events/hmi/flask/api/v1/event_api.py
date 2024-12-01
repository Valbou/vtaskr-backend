from datetime import timedelta

from flask import current_app, g, request
from src.events.hmi.dto import EventDTOMapperDTO
from src.events.services import EventsService
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import list_dto_to_dict, list_models_to_list_dto
from src.libs.iam.flask.config import login_required
from src.libs.redis import rate_limited

from .. import V1, events_bp, logger


@events_bp.route(f"{V1}/events/events/<string:tenant_id>", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=10))
def get_events(tenant_id: str):
    """Get all events of a tenant_id"""

    event_service = EventsService(current_app.dependencies)

    if request.method == "GET":
        events = event_service.get_all_tenant_events(user_id=g.user.id, tenant_id=tenant_id)
        events_dto = list_models_to_list_dto(EventDTOMapperDTO, events)

        return ResponseAPI.get_response(list_dto_to_dict(events_dto), 200)

    else:
        return ResponseAPI.get_405_response()
