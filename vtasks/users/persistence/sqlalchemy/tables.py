from datetime import datetime


from sqlalchemy import Table, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from vtasks.users.models import User, Token
from vtasks.sqlalchemy.base import mapper_registry


user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String(25)),
    Column("last_name", String(25)),
    Column("email", String(250), unique=True),
    Column("hash_password", String(256)),
    Column("created_at", DateTime, default=datetime.now()),
    Column("last_login_at", DateTime, nullable=True, default=None),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={"tokens": relationship("Token", back_populates="user")},
)


token_table = Table(
    "tokens",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime, default=datetime.now()),
    Column("last_activity_at", DateTime, default=datetime.now()),
    Column("sha_token", String(64), unique=True),
    Column("user_id", ForeignKey("users.id")),
)

mapper_registry.map_imperatively(
    Token,
    token_table,
    properties={"user": relationship("User", back_populates="tokens")},
)
