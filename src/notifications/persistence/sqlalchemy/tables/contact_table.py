from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.notifications.models import Contact

contact_table = Table(
    "contacts",
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
    Column("email", String(250), nullable=False),
    Column("telegram", String(90), nullable=False),
    Column("phone_number", String(20), nullable=False),
)


mapper_registry.map_imperatively(
    Contact,
    contact_table,
    properties={
        "subscriptions": relationship(
            "Subscription", back_populates="contact", passive_deletes=False
        ),
    },
)
