from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, String, Table, types

from src.libs.sqlalchemy.base import mapper_registry
from src.logtrail.models import LogTrail

logtrails_table = Table(
    "logtrails",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at", DateTime(timezone=True), default=datetime.now(tz=ZoneInfo("UTC"))
    ),
    Column("tenant_id", String, nullable=False),
    Column("separator", String(5), nullable=False),
    Column("log_type", String, nullable=False),
    Column("content", String, nullable=True),
    Column("event", types.JSON, nullable=True),
)


mapper_registry.map_imperatively(
    LogTrail,
    logtrails_table,
)
