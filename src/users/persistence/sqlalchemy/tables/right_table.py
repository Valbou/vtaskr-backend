from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    Column,
    DateTime,
    Dialect,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    UniqueConstraint,
    types,
)
from sqlalchemy.orm import relationship

from src.libs.iam.constants import Permissions, Resources
from src.libs.sqlalchemy.base import mapper_registry
from src.users.models.right import Right


class PermissionsType(types.TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(
        self, value: list[Permissions] | Permissions, dialect: Dialect
    ) -> int:
        return sum([perm.value for perm in value]) if isinstance(value, list) else value

    def process_result_value(self, value: int, dialect: Dialect) -> list[Permissions]:
        return [perm for perm in Permissions if value & perm]


right_table = Table(
    "rights",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at", DateTime(timezone=True), default=datetime.now(tz=ZoneInfo("UTC"))
    ),
    Column(
        "roletype_id",
        String,
        ForeignKey("roletypes.id", ondelete="CASCADE", name="fk_rights_roletype_id"),
        nullable=False,
    ),
    Column("resource", Enum(Resources), nullable=False),
    Column("permissions", PermissionsType, nullable=False),
    UniqueConstraint("roletype_id", "resource", name="right_roletype_resource"),
    Index("right_roletype_resource_index", "roletype_id", "resource"),
)


mapper_registry.map_imperatively(
    Right,
    right_table,
    properties={
        "roletype": relationship(
            "RoleType", back_populates="rights", passive_deletes=True
        ),
    },
)
