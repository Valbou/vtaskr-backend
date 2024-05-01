from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, String, Table, types

from src.libs.sqlalchemy.base import mapper_registry
from src.events.models import Event

events_table = Table(
    "events",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("tenant_id", String, nullable=False),
    Column("name", String, nullable=False),
    Column("data", types.JSON, nullable=True),
)


mapper_registry.map_imperatively(
    Event,
    events_table,
)
