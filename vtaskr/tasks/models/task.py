from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, TypeVar

from pytz import utc

from vtaskr.libs.secutity.utils import get_id

from .tag import Tag


class EisenhowerFlag(Enum):
    DO = "todo"
    SCHEDULE = "toschedule"
    DELEGATE = "todelegate"
    DELETE = "todelete"


T = TypeVar("T", bound="Task")


@dataclass
class Task:
    id: str = ""
    created_at: Optional[datetime] = None
    user_id: str = ""
    title: str = ""
    description: str = ""
    emergency: bool = False
    important: bool = False
    scheduled_at: Optional[datetime] = None
    duration: Optional[timedelta] = None
    done: Optional[datetime] = None
    tags: Optional[list[Tag]] = None

    def __init__(
        self,
        user_id: str,
        title: str,
        description: str = "",
        emergency: bool = False,
        important: bool = False,
        scheduled_at: Optional[datetime] = None,
        duration: Optional[timedelta] = None,
        done: Optional[datetime] = None,
        id: str = "",
        created_at: Optional[datetime] = None,
        tags: Optional[list[Tag]] = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.user_id = user_id
        self.title = title
        self.description = description
        self.emergency = emergency
        self.important = important
        self.scheduled_at = scheduled_at
        self.duration = duration
        self.done = done
        self.tags = tags or []

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
