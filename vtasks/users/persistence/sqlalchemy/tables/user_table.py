from datetime import datetime
from pytz import utc

from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.orm import relationship

from vtasks.users.models import User
from vtasks.sqlalchemy.base import mapper_registry


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String(25)),
    Column("last_name", String(25)),
    Column("email", String(250), unique=True),
    Column("hash_password", String(256)),
    Column("locale", String(5)),
    Column("created_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("last_login_at", DateTime(timezone=True), nullable=True, default=None),
)


mapper_registry.map_imperatively(
    User,
    user_table,
    properties={"tokens": relationship("Token", back_populates="user")},
)
