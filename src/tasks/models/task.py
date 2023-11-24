from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import TypeVar
from zoneinfo import ZoneInfo

from src.libs.security.utils import get_id

from .tag import Tag


class EisenhowerFlag(Enum):
    DO = "todo"
    SCHEDULE = "toschedule"
    DELEGATE = "todelegate"
    DELETE = "todelete"


T = TypeVar("T", bound="Task")


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
