from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pytz import utc

from src.colors.models.color import Color
from src.libs.security.utils import get_id


@dataclass
class Tag:
    title: str
    tenant_id: str
    color: Color | None = None
    tasks: list[Any] = field(default_factory=list)
    id: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        self.color = self.color or Color("#000000", "#FFFFFF")
        self.id = self.id or get_id()
        self.created_at = self.created_at or datetime.now(utc)

    def add_tasks(self, tasks: list):
        self.tasks.extend(tasks)

    def remove_tasks(self, tasks_id: list[str]):
        self.tasks = [t for t in self.tasks if t.id not in tasks_id]

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f"<Tag {self.title!r}>"
