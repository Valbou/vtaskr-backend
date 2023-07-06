import os

from redis import Redis, from_url


class NoSQLSession:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def __enter__(self):
        self.pipe = self.redis.pipeline()
        return self.pipe

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipe.execute()


class NoSQLService:
    def get_database_url(self) -> str:
        CACHE_TYPE = os.getenv("CACHE_TYPE")
        CACHE_HOST = os.getenv("CACHE_HOST")
        CACHE_PORT = os.getenv("CACHE_PORT")
        CACHE_NAME = os.getenv("CACHE_NAME")

        return f"{CACHE_TYPE}://{CACHE_HOST}:{CACHE_PORT}/{CACHE_NAME}"

    def get_engine(self) -> Redis:
        return from_url(self.get_database_url())

    def get_session(self) -> NoSQLSession:
        return NoSQLSession(self.get_engine())


class TestNoSQLService(NoSQLService):
    def get_database_url(self) -> str:
        CACHE_TYPE = os.getenv("CACHE_TYPE")
        CACHE_HOST = os.getenv("CACHE_HOST")
        CACHE_PORT = os.getenv("CACHE_PORT")
        CACHE_NAME = os.getenv("CACHE_TEST")

        return f"{CACHE_TYPE}://{CACHE_HOST}:{CACHE_PORT}/{CACHE_NAME}"
