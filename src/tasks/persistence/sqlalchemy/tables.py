from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Interval, String, Table
from sqlalchemy.orm import relationship

from src.colors.persistence.sqlalchemy.color import ColorType
from src.libs.sqlalchemy.base import mapper_registry
from src.tasks import Tag, Task

tasktag_table = Table(
    "taskstags",
    mapper_registry.metadata,
    Column(
        "tag_id",
        String,
        ForeignKey("tags.id", name="fk_taskstags_tag_id"),
        primary_key=True,
    ),
    Column(
        "task_id",
        String,
        ForeignKey("tasks.id", name="fk_taskstags_task_id"),
        primary_key=True,
    ),
)


tag_table = Table(
    "tags",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("tenant_id", String, nullable=False),
    Column("title", String(50), nullable=False),
    Column("color", ColorType),
)


mapper_registry.map_imperatively(
    Tag,
    tag_table,
    properties={
        "tasks": relationship(
            Task,
            secondary=tasktag_table,
            back_populates="tags",
            lazy="subquery",
            join_depth=1,
        )
    },
)


tasks_table = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column("tenant_id", String, nullable=False),
    Column("title", String(150), nullable=False),
    Column("description", String, nullable=False, default=""),
    Column("emergency", Boolean, nullable=False, default=False),
    Column("important", Boolean, nullable=False, default=False),
    Column("scheduled_at", DateTime(timezone=True), nullable=True, default=None),
    Column("duration", Interval, nullable=True, default=None),
    Column("done", DateTime(timezone=True), nullable=True, default=None),
    Column("assigned_to", String, nullable=False),
)


mapper_registry.map_imperatively(
    Task,
    tasks_table,
    properties={
        "tags": relationship(
            Tag,
            secondary=tasktag_table,
            back_populates="tasks",
            lazy="subquery",
            join_depth=1,
        )
    },
)
