"""
A task is a basic item to register a thing to do in the futur.

A quick task that take no time to do and/or not need to be scheduled (like: call mom)
It's for a basic to do list without strong priority, it's just a reminder.

A long task may need to be scheduled, timed and may have dependencies.
It's more a project management.

Real life mix quick and long tasks, a relatively long task like
write a new code feature, may come with some quick tasks:
check code quality, check tests are ok, check variable names etc...
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

from src.libs.security.utils import get_id

from .tag import Tag

# TODO: Add some features like:
# - A parent blocking task (M2M)
# - A deadline
# - A progress
# - A project (FK)
# - A frequency (FK)
# - A reminder (FK)
# - A trigger (M2M)


class EisenhowerFlag(Enum):
    DO = "todo"
    SCHEDULE = "toschedule"
    DELEGATE = "todelegate"
    DELETE = "todelete"


@dataclass
class Task:
    title: str
    tenant_id: str
    description: str = ""
    emergency: bool = False
    important: bool = False
    scheduled_at: datetime | None = None
    duration: timedelta | None = None
    done: datetime | None = None
    assigned_to: str = ""
    tags: list[Tag] = field(default_factory=list)
    id: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(tz=ZoneInfo("UTC"))

    def is_done(self) -> bool:
        return bool(self.done)

    def get_eisenhower_flag(self):
        if self.emergency and self.important:
            return EisenhowerFlag.DO
        elif not self.emergency and self.important:
            return EisenhowerFlag.SCHEDULE
        elif self.emergency and not self.important:
            return EisenhowerFlag.DELEGATE
        return EisenhowerFlag.DELETE

    def add_tags(self, tags: list[Tag]):
        self.tags.extend(tags)

    def remove_tags(self, tags_id: list[str]):
        self.tags = [t for t in self.tags if t.id not in tags_id]

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f"<Tag {self.title!r}>"
