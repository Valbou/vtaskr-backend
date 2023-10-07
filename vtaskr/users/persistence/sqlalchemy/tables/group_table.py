from datetime import datetime

from pytz import utc
from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.orm import relationship

from vtaskr.libs.sqlalchemy.base import mapper_registry
from vtaskr.users.models import Group

group_table = Table(
    "groups",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at", DateTime(timezone=True), default=datetime.now(utc), nullable=False
    ),
    Column("name", String(80), nullable=False),
)


mapper_registry.map_imperatively(
    Group,
    group_table,
    properties={
        "roles": relationship("Role", back_populates="group"),
        "roletypes": relationship("RoleType", back_populates="group"),
    },
)
