import os
from enum import Enum
from typing import Optional, Union, Literal

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from .base import mapper_registry


class DBType(Enum):
    TEST = "test"
    PROD = "prod"


class SQLService:
    def __init__(
        self,
        database: Optional[DBType] = None,
        echo: Union[None, bool, Literal["debug"]] = False,
    ) -> None:
        debug = False
        if os.getenv("DEBUG_SQL") == "true":
            debug = bool(os.getenv("DEBUG_SQL"))
        elif os.getenv("DEBUG_SQL") == "debug":
            debug = os.getenv("DEBUG_SQL")

        self.echo: Union[None, bool, Literal["debug"]] = echo or debug
        self.database: Optional[DBType] = database
        self.mapping()

    def get_database_url(self) -> str:
        DB_TYPE = os.getenv("DB_TYPE")
        BD_DRIVER = os.getenv("BD_DRIVER")
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASS")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = (
            os.getenv("DB_NAME")
            if self.database == DBType.PROD
            else os.getenv("DB_TEST")
        )

        return (
            f"{DB_TYPE}+{BD_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    def mapping(self):
        from vtasks.users.persistence.sqlalchemy.tables import user_table

    def get_engine(self) -> Engine:
        return create_engine(self.get_database_url(), pool_size=20, echo=self.echo)

    def get_session(self) -> Session:
        return sessionmaker(self.get_engine())()

    def create_tables(self):
        mapper_registry.metadata.create_all(bind=self.get_engine())

    def drop_tables(self):
        mapper_registry.metadata.drop_all(bind=self.get_engine())
