from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Boolean, Column, DateTime, Enum, String, Table

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import RequestChange, RequestType

request_change_table = Table(
    "requestschanges",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("request_type", Enum(RequestType), nullable=False),
    Column("email", String, nullable=False),
    Column("code", String(12), nullable=False),
    Column("done", Boolean, default=False),
)


mapper_registry.map_imperatively(
    RequestChange,
    request_change_table,
)
