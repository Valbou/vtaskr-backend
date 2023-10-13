from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pytz import utc

from vtaskr.colors.models.color import Color
from vtaskr.libs.secutity.utils import get_id


@dataclass
class Tag:
    id: str = ""
    created_at: datetime | None = None
    tenant_id: str = ""
    title: str = ""
    color: Color | None = None
    tasks: list[Any] | None = None

    def __init__(
        self,
        tenant_id: str,
        title: str,
        color: Color | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        tasks: list[Any] | None = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.tenant_id = tenant_id
        self.title = title
        self.color = color or Color("#000000", "#FFFFFF")
        self.tasks = tasks or []

    def add_tasks(self, tasks: list):
        self.tasks.extend(tasks)

    def remove_tasks(self, tasks_id: list[str]):
        self.tasks = [t for t in self.tasks if t.id not in tasks_id]

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f"<Tag {self.title!r}>"
