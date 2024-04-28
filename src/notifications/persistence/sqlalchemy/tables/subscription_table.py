from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Enum, Index, String, Table, UniqueConstraint

from src.libs.sqlalchemy.base import mapper_registry
from src.notifications.models import Subscription
from src.ports import MessageType

subscription_table = Table(
    "subscriptions",
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
    Column("tenant_id", String(90), nullable=False),
    Column("to", String, nullable=False),
    Column("cc", String, nullable=False),
    Column("bcc", String, nullable=False),
    Column("event_name", String(150), nullable=False),
    Column("event_type", Enum(MessageType), nullable=False),
    UniqueConstraint("event_name", "event_type", "to", name="subscriptions_events_to"),
    Index(
        "subscriptions_events_to_index", "event_name", "event_type", "to", unique=True
    ),
)


mapper_registry.map_imperatively(
    Subscription,
    subscription_table,
)
