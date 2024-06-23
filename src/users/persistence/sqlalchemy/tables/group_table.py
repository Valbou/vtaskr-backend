from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Boolean, Column, DateTime, String, Table
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import Group

group_table = Table(
    "groups",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("name", String(80), nullable=False),
    Column("description", String, default="", nullable=False),
    Column("is_private", Boolean, default=True),
)


mapper_registry.map_imperatively(
    Group,
    group_table,
    properties={
        "roles": relationship("Role", back_populates="group", passive_deletes=True),
        "roletypes": relationship(
            "RoleType", back_populates="group", passive_deletes=True
        ),
        "invitations": relationship(
            "Invitation", back_populates="on_group", passive_deletes=True
        ),
    },
)
