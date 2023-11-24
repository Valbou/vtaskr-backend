from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import RoleType

roletype_table = Table(
    "roletypes",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at", DateTime(timezone=True), default=datetime.now(tz=ZoneInfo("UTC"))
    ),
    Column("name", String(80), nullable=False),
    Column(
        "group_id",
        String,
        ForeignKey("groups.id", ondelete="CASCADE", name="fk_roletypes_group_id"),
        nullable=True,
    ),
    UniqueConstraint("name", "group_id", name="roletype_name_group"),
    Index("roletype_name_group_index", "name", "group_id"),
)


mapper_registry.map_imperatively(
    RoleType,
    roletype_table,
    properties={
        "group": relationship(
            "Group", back_populates="roletypes", passive_deletes=True
        ),
        "rights": relationship(
            "Right", back_populates="roletype", passive_deletes=True
        ),
        "roles": relationship("Role", back_populates="roletype", passive_deletes=True),
    },
)
