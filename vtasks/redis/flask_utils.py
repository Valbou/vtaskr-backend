from datetime import timedelta
from typing import Optional

from redis import Redis
from flask import Request

from vtasks.flask.utils import get_ip
from .ratelimit import RateLimit


def rate_limit(
    redis: Redis,
    request: Request,
    token: str,
    hit: int = 1,
    period: Optional[timedelta] = None,
):
    identifier = token or get_ip(request)
    path = f"{request.method}:{request.path}"
    period = period or timedelta(seconds=1)
    RateLimit(redis, identifier, path, hit, period)()
