from datetime import datetime

from pytz import utc
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Dialect,
    ForeignKey,
    Interval,
    String,
    Table,
    types,
)
from sqlalchemy.orm import relationship

from vtaskr.sqlalchemy.base import mapper_registry
from vtaskr.tasks import Color, Tag, Task


class ColorType(types.TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Color, dialect: Dialect) -> str:
        return str(value)

    def process_result_value(self, value: str, dialect: Dialect) -> Color:
        return Color.from_string(value)


tasktag_table = Table(
    "taskstags",
    mapper_registry.metadata,
    Column("tag_id", String, ForeignKey("tags.id"), primary_key=True),
    Column("task_id", String, ForeignKey("tasks.id"), primary_key=True),
)


tag_table = Table(
    "tags",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("user_id", String, ForeignKey("users.id")),
    Column("title", String(50)),
    Column("color", ColorType),
)


mapper_registry.map_imperatively(
    Tag,
    tag_table,
    properties={
        "tasks": relationship(Task, secondary=tasktag_table, back_populates="tags")
    },
)


tasks_table = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime(timezone=True), default=datetime.now(utc)),
    Column("user_id", String, ForeignKey("users.id")),
    Column("title", String(150)),
    Column("description", String),
    Column("emergency", Boolean, default=False),
    Column("important", Boolean, default=False),
    Column("scheduled_at", DateTime(timezone=True), nullable=True, default=None),
    Column("duration", Interval, nullable=True, default=None),
    Column("done", DateTime(timezone=True), nullable=True, default=None),
)


mapper_registry.map_imperatively(
    Task,
    tasks_table,
    properties={
        "tags": relationship(Tag, secondary=tasktag_table, back_populates="tasks")
    },
)
