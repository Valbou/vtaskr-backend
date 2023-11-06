from datetime import timedelta

from flask import current_app, g
from src.libs.flask.utils import ResponseAPI
from src.libs.redis import rate_limited
from src.users.hmi.flask.decorators import login_required
from src.users.services import UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "delete": {
        "description": "Delete a valid token",
        "summary": "To logout an user",
        "operationId": "deleteLogout",
        "responses": {
            "204": {
                "description": "no response content",
                "content": {},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
    }
}
openapi.register_path(f"{V1}/users/logout", api_item)


@users_bp.route(f"{V1}/users/logout", methods=["DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=6, period=timedelta(seconds=60))
def logout():
    """
    URL to logout a logged in user - Token required

    Need a valid token
    Return a 204
    """
    with current_app.sql.get_session() as session:
        auth_service = UserService(session)
        if auth_service.logout(g.token):
            data = {}
            return ResponseAPI.get_response(data, 204)
        else:
            return ResponseAPI.get_403_response("Unauthorized")
