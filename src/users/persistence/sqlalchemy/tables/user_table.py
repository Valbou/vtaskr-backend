from datetime import datetime
from zoneinfo import ZoneInfo

from babel import Locale
from sqlalchemy import Column, DateTime, Dialect, String, Table, types
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import User


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
    Column("first_name", String(25), nullable=False),
    Column("last_name", String(25), nullable=False),
    Column("email", String(250), unique=True, nullable=False),
    Column("hash_password", String(256)),
    Column("locale", LocaleField),
    Column("timezone", String(35)),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("last_login_at", DateTime(timezone=True), nullable=True, default=None),
)


mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "tokens": relationship("Token", back_populates="user", passive_deletes=True),
        "roles": relationship("Role", back_populates="user", passive_deletes=True),
    },
)
