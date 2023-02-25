from unittest import TestCase
from datetime import timedelta

from vtasks.redis.database import NoSQLService
from vtasks.redis.ratelimit import RateLimit, LimitExceededError


class TestRateLimit(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.nosql = NoSQLService(testing=True)
        self.redis = self.nosql.get_engine()

    def test_simple_call_do_nothing(self):
        rl = RateLimit(self.redis, "::1", "/test_1", 1, timedelta(seconds=1))
        self.assertIsNone(rl())

    def test_over_limit(self):
        rl = RateLimit(self.redis, "::1", "/", 1, timedelta(seconds=1))
        rl()
        with self.assertRaises(LimitExceededError):
            rl()
