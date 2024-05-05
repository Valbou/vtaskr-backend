from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Enum, Index, String, Table, UniqueConstraint

from src.libs.sqlalchemy.base import mapper_registry
from src.notifications.models import Template
from src.ports import MessageType

template_table = Table(
    "templates",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("name", String(90), nullable=False),
    Column("sender", String(150), nullable=False),
    Column("subject", String(150), nullable=False),
    Column("html", String(150), nullable=False),
    Column("text", String(150), nullable=False),
    Column("event_name", String(150), nullable=False),
    Column("event_type", Enum(MessageType), nullable=False),
    UniqueConstraint("event_name", "event_type", name="templates_events"),
    Index("templates_events_index", "event_name", "event_type", unique=True),
)


mapper_registry.map_imperatively(
    Template,
    template_table,
)
