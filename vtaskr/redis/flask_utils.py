from datetime import timedelta
from functools import wraps
from logging import Logger
from typing import Callable

from flask import current_app, g, request

from vtaskr.flask.utils import ResponseAPI, get_ip
from vtaskr.redis.ratelimit import LimitExceededError, RateLimit


def rate_limited(
    logger: Logger, hit: int = 1, period: timedelta = timedelta(seconds=1)
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = g.token if hasattr(g, "token") else None
            identifier = token or get_ip(request)
            path = f"{request.method}:{request.path}"

            try:
                RateLimit(
                    current_app.nosql.get_engine(), identifier, path, hit, period
                )()
                return func(*args, **kwargs)
            except LimitExceededError as e:
                logger.warning(str(e))
                return ResponseAPI.get_error_response("Too many requests", 429)

        return wrapper

    return decorator
