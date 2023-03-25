from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

from .tag import Tag


class EisenhowerFlag(Enum):
    TODO = "todo"
    SCHEDULE = "toschedule"
    DELEGATE = "todelegate"
    DELETE = "todelete"


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
        self.id = id or uuid4().hex
        self.created_at = created_at or datetime.now()
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
            return EisenhowerFlag.TODO
        elif not self.emergency and self.important:
            return EisenhowerFlag.SCHEDULE
        elif self.emergency and not self.important:
            return EisenhowerFlag.DELEGATE
        return EisenhowerFlag.DELETE
