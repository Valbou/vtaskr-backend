from datetime import timedelta
from typing import Optional, Callable
from functools import wraps
from logging import Logger

from flask import current_app, request, g

from vtasks.flask.utils import get_ip, ResponseAPI
from vtasks.redis.ratelimit import RateLimit, LimitExceededError


def rate_limited(logger: Logger, hit: int = 1, period: Optional[timedelta] = None):
    period = period or timedelta(seconds=1)

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
