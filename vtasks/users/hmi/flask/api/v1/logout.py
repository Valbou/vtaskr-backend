from datetime import timedelta

from flask import current_app, g

from vtasks.flask.utils import ResponseAPI
from vtasks.redis import rate_limited
from vtasks.users.hmi.user_service import UserService
from vtasks.users.hmi.flask.decorators import login_required

from .. import users_bp, logger, V1


@users_bp.route(f"{V1}/users/logout", methods=["DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=6, period=timedelta(seconds=60))
def logout():
    """
    URL to logout a logged in user - Token required

    Need a valid token
    Return a 204
    """
    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            if auth_service.logout(g.token):
                data = {}
                return ResponseAPI.get_response(data, 204)
            else:
                return ResponseAPI.get_error_response("Unauthorized", 403)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)
