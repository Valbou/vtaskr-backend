from datetime import timedelta

from flask import current_app, request
from src.libs.flask.utils import ResponseAPI, get_bearer_token
from src.libs.redis import rate_limited
from src.users.services import TokenService

from .. import V1, logger, openapi, users_bp

api_item = {
    "post": {
        "description": "Secure user auth with 2FA confirmation",
        "summary": "To confirm 2FA auth",
        "operationId": "postConfirm2FA",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {},
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Code to confirm user identity",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code_2FA": {
                                "type": "string",
                                "example": "1A2b3C",
                            },
                        },
                        "required": [
                            "code_2FA",
                        ],
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/2fa", api_item)


@users_bp.route(f"{V1}/users/2fa", methods=["POST"])
@rate_limited(logger=logger, hit=3, period=timedelta(seconds=60))
def confirm_2fa():
    """
    URL to confirm 2FA auth - Token required

    Need a valid temp token and a code
    Return a 200
    """
    sha_token = get_bearer_token(request)
    if not sha_token:
        return ResponseAPI.get_401_response("Invalid token")

    payload: dict = request.get_json()

    try:
        code = payload.get("code_2FA")
    except AttributeError as e:
        logger.warning(f"400 Error: {e}")
        return ResponseAPI.get_400_response()

    try:
        with current_app.sql.get_session() as session:
            token_service = TokenService(session=session)
            token = token_service.get_token(sha_token)

            if code and token and token.is_temp_valid() and token.validate_token(code):
                session.commit()
                data = {}
                return ResponseAPI.get_response(data, 200)
            else:
                logger.warning("401 Error: Attempt with bad 2FA")
                return ResponseAPI.get_401_response("Invalid 2FA code")
    except Exception as e:
        logger.error(f"500 Error: {e}")
        return ResponseAPI.get_500_response()
