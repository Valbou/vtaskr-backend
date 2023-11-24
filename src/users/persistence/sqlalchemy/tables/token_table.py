from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import Token

token_table = Table(
    "tokens",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column(
        "last_activity_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("temp", Boolean, nullable=False),
    Column("temp_code", String(12)),
    Column("sha_token", String(64), unique=True, nullable=False),
    Column(
        "user_id",
        String,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_tokens_user_id"),
        nullable=False,
    ),
)


mapper_registry.map_imperatively(
    Token,
    token_table,
    properties={
        "user": relationship("User", back_populates="tokens", passive_deletes=True)
    },
)
