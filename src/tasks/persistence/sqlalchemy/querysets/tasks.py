from datetime import datetime
from typing import Self

from src.tasks.models import Tag, Task

from .tenant_queryset import TenantQueryset


class TaskQueryset(TenantQueryset):
    def __init__(self):
        super().__init__(Task)

    def tag(self, tag_id: str) -> Self:
        self._query = self._query.where(self.qs_class.tags.any(Tag.id == tag_id))

        return self

    def scheduled_in(self, start: datetime, end: datetime) -> Self:
        self._query = self._query.where(
            self.qs_class.scheduled_at != None,  # noqa: E711
            self.qs_class.scheduled_at >= start,
            self.qs_class.scheduled_at < end,
        )

        return self
