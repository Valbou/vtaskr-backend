from dataclasses import dataclass
from datetime import datetime
from re import fullmatch
from typing import Any, List, Optional, TypeVar

from pytz import utc

from vtaskr.libs.secutity.utils import get_id


class ColorFormatError(Exception):
    pass


TColor = TypeVar("TColor", bound="Color")


class Color:
    background: str
    text: str

    def __init__(self, background: str, text: str) -> None:
        if Color.check_format(background) and Color.check_format(text):
            self.background = background
            self.text = text
        else:
            raise ColorFormatError

    def __str__(self) -> str:
        return f"{self.background}|{self.text}"

    @classmethod
    def from_string(cls, colors: str) -> Optional[TColor]:
        return Color(*colors.split("|"))

    @classmethod
    def check_format(cls, color) -> bool:
        match = fullmatch(r"^#[0-9A-Fa-f]{6}$", color)
        if match:
            return True
        return False


@dataclass
class Tag:
    id: str = ""
    created_at: Optional[datetime] = None
    user_id: str = ""
    title: str = ""
    color: Optional[Color] = None
    tasks: Optional[List[Any]] = None

    def __init__(
        self,
        user_id: str,
        title: str,
        color: Optional[Color] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        tasks: Optional[List[Any]] = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.user_id = user_id
        self.title = title
        self.color = color or Color("#000000", "#FFFFFF")
        self.tasks = tasks or []

    def add_tasks(self, tasks: list):
        self.tasks.extend(tasks)

    def remove_tasks(self, tasks_id: List[str]):
        self.tasks = [t for t in self.tasks if t.id not in tasks_id]

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f"<Tag {self.title!r}>"
