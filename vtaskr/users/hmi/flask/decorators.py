from functools import wraps
from logging import Logger
from typing import Callable

from flask import current_app, g, request

from vtaskr.flask.utils import ResponseAPI, get_bearer_token
from vtaskr.users.hmi.user_service import UserService


def login_required(logger: Logger):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                sha_token = get_bearer_token(request)
                if not sha_token:
                    return ResponseAPI.get_error_response("Invalid token", 401)

                with current_app.sql.get_session() as session:
                    session.expire_on_commit = False
                    auth_service = UserService(session, testing=current_app.testing)
                    user = auth_service.user_from_token(sha_token)
                    if user:
                        g.token = sha_token
                        g.user = user
                    else:
                        return ResponseAPI.get_error_response("Invalid token", 401)
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(str(e))
                return ResponseAPI.get_error_response("Internal error", 500)

        return wrapper

    return decorator
