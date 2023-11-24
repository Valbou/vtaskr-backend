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

from src.colors.persistence.sqlalchemy.color import ColorType
from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import Role

role_table = Table(
    "roles",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column(
        "user_id",
        String,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_roles_user_id"),
        nullable=False,
    ),
    Column(
        "group_id",
        String,
        ForeignKey("groups.id", ondelete="CASCADE", name="fk_roles_group_id"),
        nullable=False,
    ),
    Column(
        "roletype_id",
        String,
        ForeignKey("roletypes.id", ondelete="RESTRICT", name="fk_roles_roletype_id"),
        nullable=False,
    ),
    Column("color", ColorType, nullable=True),
    UniqueConstraint("user_id", "group_id", name="role_user_group"),
    Index("role_user_group_index", "user_id", "group_id"),
)


mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "user": relationship("User", back_populates="roles", passive_deletes=True),
        "group": relationship("Group", back_populates="roles", passive_deletes=True),
        "roletype": relationship(
            "RoleType", back_populates="roles", passive_deletes=True
        ),
    },
)
