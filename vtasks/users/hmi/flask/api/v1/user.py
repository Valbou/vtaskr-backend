from datetime import timedelta

from flask import current_app, g, request

from vtasks.flask.utils import ResponseAPI
from vtasks.redis import rate_limited
from vtasks.secutity.validators import PasswordComplexityError
from vtasks.users.hmi.dto import UserDTO, UserMapperDTO
from vtasks.users.hmi.flask.decorators import login_required
from vtasks.users.persistence import UserDB

from .. import V1, logger, users_bp


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
            user_dto = UserMapperDTO.model_to_dto(g.user)
            return ResponseAPI.get_response(UserMapperDTO.dto_to_dict(user_dto), 200)

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
                user_dto = UserDTO(**request.get_json())
                g.user = UserMapperDTO.dto_to_model(user_dto, g.user)
                user_db.update(session, g.user)
                user_dto = UserMapperDTO.model_to_dto(g.user)
            return ResponseAPI.get_response(UserMapperDTO.dto_to_dict(user_dto), 200)

    except PasswordComplexityError as e:
        return ResponseAPI.get_error_response(str(e), 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)
