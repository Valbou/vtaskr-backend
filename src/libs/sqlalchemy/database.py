from typing import Literal

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, registry, scoped_session, sessionmaker

from src.ports import SQLPort

from .base import mapper_registry
from .settings import (
    BD_DRIVER,
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_TEST,
    DB_TYPE,
    DB_USER,
    DEBUG_SQL,
)


class SQLService(SQLPort):
    def __init__(self, echo: None | bool | Literal["debug"] = False, **kwargs) -> None:
        debug = False
        if DEBUG_SQL == "true":
            debug = bool(DEBUG_SQL)
        elif DEBUG_SQL == "debug":
            debug = DEBUG_SQL

        self.echo = echo or debug
        self._repository_registry = {}
        self.mapping()

    def set_context(self, **ctx) -> None:
        repositories = ctx.get("repositories", [])
        for repository_data in repositories:
            self.register_repository(*repository_data)

    def get_database_url(self) -> str:
        return (
            f"{DB_TYPE}+{BD_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    def mapping(self) -> None:
        """Import all sqlalchemy tables here to set registry mapping"""
        from .declare_tables import INIT

    def get_engine(self) -> Engine:
        return create_engine(self.get_database_url(), pool_size=20, echo=self.echo)

    def get_session(self, expire_on_commit=False) -> Session:
        return scoped_session(
            sessionmaker(self.get_engine(), expire_on_commit=expire_on_commit)
        )()

    def get_registry(self) -> registry:
        return mapper_registry

    def create_tables(self) -> None:
        mapper_registry.metadata.create_all(bind=self.get_engine())

    def drop_tables(self) -> None:
        mapper_registry.metadata.drop_all(bind=self.get_engine())


class TestSQLService(SQLService):
    def get_database_url(self) -> str:
        return (
            f"{DB_TYPE}+{BD_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST}"
        )
