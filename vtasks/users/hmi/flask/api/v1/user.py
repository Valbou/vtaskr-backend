from datetime import timedelta

from flask import current_app, g, request

from vtasks.flask.utils import ResponseAPI
from vtasks.redis import rate_limited
from vtasks.secutity.validators import PasswordComplexityError
from vtasks.users.persistence import UserDB
from vtasks.users.hmi.flask.decorators import login_required

from .. import users_bp, logger, V1


@users_bp.route(f"{V1}/users/me", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def me():
    """
    URL to get current user informations - Token required

    Need a valid token
    Return a jsonify user
    """
    try:
        if g.user:
            data = g.user.to_external_data()
            return ResponseAPI.get_response(data, 200)
        else:
            return ResponseAPI.get_error_response("Invalid token", 403)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/me/update", methods=["PUT", "PATCH"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def update_me():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """
    try:
        if g.user is None:
            return ResponseAPI.get_error_response("Invalid token", 401)
        else:
            user_db = UserDB()
            with current_app.sql.get_session() as session:
                g.user.from_external_data(request.get_json())
                user_db.update(session, g.user)
                data = g.user.to_external_data()
            return ResponseAPI.get_response(data, 200)
    except PasswordComplexityError as e:
        return ResponseAPI.get_error_response(str(e), 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)
