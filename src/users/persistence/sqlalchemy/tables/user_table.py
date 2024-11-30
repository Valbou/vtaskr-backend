from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.orm import relationship

from src.libs.babel.sqlalchemy_utils import LocaleField
from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import User

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
        "tokens": relationship(
            "Token", back_populates="user", cascade="all, delete-orphan"
        ),
        "roles": relationship(
            "Role", back_populates="user", cascade="all, delete-orphan"
        ),
        "invitations": relationship(
            "Invitation", back_populates="from_user", cascade="all, delete-orphan"
        ),
    },
)
