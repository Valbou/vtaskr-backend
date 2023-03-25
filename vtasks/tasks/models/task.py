from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, TypeVar

from dateutil import parser
from pytz import utc

from vtasks.secutity.utils import get_id

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
    tags: Optional[List[Tag]] = None
    # reccurence
    # rappels
    # sub tasks

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
        tags: Optional[List[Tag]] = None,
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

    def to_external_data(self, with_tags=False) -> dict:
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "emergency": self.emergency,
            "important": self.important,
            "scheduled_at": self.scheduled_at.isoformat()
            if self.scheduled_at
            else None,
            "duration": self.duration.total_seconds() if self.duration else None,
            "done": self.done,
        }
        if with_tags:
            data["tags"] = [t.to_external_data() for t in self.tags]
        return data

    @classmethod
    def from_external_data(cls, user_id: str, task_dict: dict) -> T:
        schedule = None
        if task_dict.get("scheduled_at", None):
            schedule = parser.parse(task_dict.get("scheduled_at"))

        duration = None
        if task_dict.get("duration", None):
            duration = timedelta(seconds=task_dict.get("duration"))

        done = None
        if task_dict.get("done", None):
            done = parser.parse(task_dict.get("done"))

        return Task(
            user_id=user_id,
            title=task_dict.get("title", "---"),
            description=task_dict.get("description", ""),
            emergency=task_dict.get("emergency", False),
            important=task_dict.get("important", False),
            scheduled_at=schedule,
            duration=duration,
            done=done,
        )
