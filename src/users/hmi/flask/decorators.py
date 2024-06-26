from functools import wraps
from logging import Logger
from typing import Callable

from flask import current_app, g, request
from src.libs.flask.utils import ResponseAPI, get_auth_token
from src.libs.iam.config import PermissionError
from src.users.services import UserService


def login_required(logger: Logger):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                sha_token = get_auth_token(request)
                if not sha_token:
                    return ResponseAPI.get_401_response("Invalid token")

                auth_service = UserService(services=current_app.dependencies)
                user = auth_service.user_from_token(sha_token)
                if user:
                    g.token = sha_token
                    g.user = user
                else:
                    return ResponseAPI.get_401_response("Invalid token")
                return func(*args, **kwargs)
            except PermissionError as e:
                logger.info(f"403 Error: {e}")
                return ResponseAPI.get_403_response("Permissions Error")
            except Exception as e:
                logger.error(f"500 Error: {e}")
                return ResponseAPI.get_500_response()

        return wrapper

    return decorator
