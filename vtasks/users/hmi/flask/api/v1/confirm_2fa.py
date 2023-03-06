from datetime import timedelta

from flask import current_app, request

from vtasks.flask.utils import ResponseAPI, get_bearer_token
from vtasks.redis import rate_limited
from vtasks.users.persistence import TokenDB

from .. import users_bp, logger, V1


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
        return ResponseAPI.get_error_response("Invalid token", 401)

    payload: dict = request.get_json()

    try:
        code = payload.get("code_2FA")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
            token_db = TokenDB()
            token = token_db.get_token(session, sha_token)
            if code and token.is_temp_valid() and token.validate_token(code):
                session.commit()
                data = {"2FA": "ok"}
                return ResponseAPI.get_response(data, 200)
            else:
                return ResponseAPI.get_error_response("Invalid 2FA code", 401)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)
