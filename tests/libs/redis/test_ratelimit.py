from datetime import timedelta
from unittest import TestCase

from src.libs.redis.database import TestNoSQLService
from src.libs.redis.ratelimit import LimitExceededError, RateLimit


class TestRateLimit(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.nosql = TestNoSQLService()
        self.redis = self.nosql.get_engine()

    def test_simple_call_do_nothing(self):
        rl = RateLimit(self.redis, "::1", "/test_1", 1, timedelta(seconds=1))
        self.assertIsNone(rl())

    def test_over_limit_1_per_sec(self):
        rl = RateLimit(self.redis, "::1", "/", 1, timedelta(seconds=1))
        rl()
        with self.assertRaises(LimitExceededError):
            rl()

    def test_over_limit_5_per_sec(self):
        rl = RateLimit(self.redis, "::1", "/", 5, timedelta(seconds=1))
        rl()
        rl()
        rl()
        rl()
        rl()
        with self.assertRaises(LimitExceededError):
            rl()
