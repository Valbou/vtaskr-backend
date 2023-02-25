from datetime import timedelta
from typing import Optional

from redis import Redis


class LimitExceededError(Exception):
    pass


class RateLimit:
    user: str = ""
    resource_name: str = ""
    period: timedelta = timedelta(seconds=1)
    limit: int = 1

    def __init__(
        self,
        redis: Redis,
        user: str,
        resource: str,
        limit: int = 1,
        period: Optional[timedelta] = None,
    ) -> None:
        self.redis = redis
        self.user = user
        self.resource_name = resource
        self.period = period or timedelta(seconds=1)
        self.limit = limit or 1

    def __call__(self):
        self.value = self._check_key()
        self._increment()

    @property
    def key(self) -> str:
        return f"{self.user}{self.resource_name}{self.period}{self.limit}"

    def _increment(self):
        self.value = self.redis.get(self.key)
        self._check_limit()
        self.redis.incr(self.key)

    def _check_key(self):
        self.value = self.redis.get(self.key)
        if self.value is None:
            self.redis.set(self.key, 0, ex=self.period)
            self.value = 0

    def _check_limit(self):
        if int(self.value) >= self.limit:
            raise LimitExceededError()
