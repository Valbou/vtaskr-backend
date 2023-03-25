from datetime import datetime

from babel import Locale
from pytz import utc
from sqlalchemy import Column, DateTime, Dialect, String, Table, types
from sqlalchemy.orm import relationship

from vtasks.sqlalchemy.base import mapper_registry
from vtasks.users.models import User


class LocaleField(types.TypeDecorator):
    impl = String(5)
    cache_ok = True

    def process_bind_param(self, value: Locale, dialect: Dialect) -> str:
        return str(value)

    def process_result_value(self, value: str, dialect: Dialect) -> Locale:
        return Locale.parse(value)


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String(25)),
    Column("last_name", String(25)),
    Column("email", String(250), unique=True),
    Column("hash_password", String(256)),
    Column("locale", LocaleField),
    Column("timezone", String(35)),
    Column("created_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("last_login_at", DateTime(timezone=True), nullable=True, default=None),
)


mapper_registry.map_imperatively(
    User,
    user_table,
    properties={"tokens": relationship("Token", back_populates="user")},
)
