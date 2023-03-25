from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    ForeignKey,
    types,
    Dialect,
    Boolean,
    Interval,
    UniqueConstraint,
)

from vtasks.tasks import Task, Tag, Color, TaskTag
from vtasks.sqlalchemy.base import mapper_registry


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
    Column("id", String, primary_key=True),
    Column("created_at", DateTime, default=datetime.now()),
    Column("tag_id", String, ForeignKey("tags.id")),
    Column("task_id", String, ForeignKey("tasks.id")),
    UniqueConstraint("tag_id", "task_id", name="tasktag_unique_association"),
)


mapper_registry.map_imperatively(
    TaskTag,
    tasktag_table,
    properties={
        "task": relationship("Task", back_populates="tags"),
        "tag": relationship("Tag", back_populates="tasks"),
    },
)


tag_table = Table(
    "tags",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime, default=datetime.now()),
    Column("user_id", String, ForeignKey("users.id")),
    Column("title", String(50)),
    Column("color", ColorType),
)


mapper_registry.map_imperatively(
    Tag,
    tag_table,
    properties={"tasks": relationship("TaskTag", back_populates="tag")},
)


tasks_table = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DateTime, default=datetime.now()),
    Column("user_id", String, ForeignKey("users.id")),
    Column("title", String(150)),
    Column("description", String),
    Column("emergency", Boolean, default=False),
    Column("important", Boolean, default=False),
    Column("scheduled_at", DateTime, nullable=True, default=None),
    Column("duration", Interval, nullable=True, default=None),
    Column("done", DateTime, nullable=True, default=None),
)


mapper_registry.map_imperatively(
    Task,
    tasks_table,
    properties={"tags": relationship("TaskTag", back_populates="task")},
)
