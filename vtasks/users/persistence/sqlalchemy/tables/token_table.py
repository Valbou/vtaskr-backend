from datetime import datetime
from pytz import utc

from sqlalchemy import Table, Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from vtasks.users.models import Token
from vtasks.sqlalchemy.base import mapper_registry


token_table = Table(
    "tokens",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("last_activity_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("temp", Boolean),
    Column("temp_code", String(12)),
    Column("sha_token", String(64), unique=True),
    Column("user_id", String, ForeignKey("users.id")),
)


mapper_registry.map_imperatively(
    Token,
    token_table,
    properties={"user": relationship("User", back_populates="tokens")},
)
