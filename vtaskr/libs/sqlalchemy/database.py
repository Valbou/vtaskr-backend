import os
from typing import Literal, Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .base import mapper_registry


class SQLService:
    def __init__(
        self,
        testing: bool = False,
        echo: Union[None, bool, Literal["debug"]] = False,
    ) -> None:
        debug = False
        if os.getenv("DEBUG_SQL") == "true":
            debug = bool(os.getenv("DEBUG_SQL"))
        elif os.getenv("DEBUG_SQL") == "debug":
            debug = os.getenv("DEBUG_SQL")

        self.echo: Union[None, bool, Literal["debug"]] = echo or debug
        self.testing = testing
        self.mapping()

    def get_database_url(self) -> str:
        DB_TYPE = os.getenv("DB_TYPE")
        BD_DRIVER = os.getenv("BD_DRIVER")
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASS")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_TEST") if self.testing else os.getenv("DB_NAME")

        return (
            f"{DB_TYPE}+{BD_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    def mapping(self):
        """Import all sqlalchemy tables here to set registry mapping"""
        from .declare_tables import INIT

    def get_engine(self) -> Engine:
        return create_engine(self.get_database_url(), pool_size=20, echo=self.echo)

    def get_session(self) -> Session:
        return scoped_session(sessionmaker(self.get_engine()))()

    def create_tables(self):
        mapper_registry.metadata.create_all(bind=self.get_engine())

    def drop_tables(self):
        mapper_registry.metadata.drop_all(bind=self.get_engine())
