from redis import Redis, from_url

from src.ports import CachePort

from .settings import CACHE_HOST, CACHE_NAME, CACHE_PORT, CACHE_TEST, CACHE_TYPE


class CacheSession:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def __enter__(self):
        self.pipe = self.redis.pipeline()
        return self.pipe

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipe.execute()


class CacheService(CachePort):
    def get_database_url(self) -> str:
        return f"{CACHE_TYPE}://{CACHE_HOST}:{CACHE_PORT}/{CACHE_NAME}"

    def get_engine(self) -> Redis:
        return from_url(self.get_database_url())

    def get_session(self) -> CacheSession:
        return CacheSession(self.get_engine())


class TestCacheService(CacheService):
    def get_database_url(self) -> str:
        return f"{CACHE_TYPE}://{CACHE_HOST}:{CACHE_PORT}/{CACHE_TEST}"
