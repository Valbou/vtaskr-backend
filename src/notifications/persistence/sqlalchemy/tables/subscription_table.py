from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.notifications.models import Subscription
from src.notifications.settings import MessageType

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
    Column(
        "contact_id",
        String,
        ForeignKey("contacts.id", ondelete="CASCADE", name="fk_subscription_contact_id"),
        nullable=False,
    ),
    Column("name", String(150), nullable=False),
    Column("type", Enum(MessageType), nullable=False),
    UniqueConstraint("name", "type", "contact_id", name="subscriptions_contact_id"),
    Index(
        "subscriptions_contact_index",
        "name",
        "type",
        "contact_id",
        unique=True,
    ),
)


mapper_registry.map_imperatively(
    Subscription,
    subscription_table,
    properties={
        "contact": relationship(
            "Contact",
            back_populates="subscriptions",
            passive_deletes=True,
            lazy="joined",
        ),
    },
)
