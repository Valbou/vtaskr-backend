from datetime import datetime

from pytz import utc
from sqlalchemy import Boolean, Column, DateTime, Enum, String, Table

from vtaskr.libs.sqlalchemy.base import mapper_registry
from vtaskr.users.models import RequestChange, RequestType

request_change_table = Table(
    "requestschanges",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at", DateTime(timezone=True), default=datetime.now(utc), nullable=False
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
