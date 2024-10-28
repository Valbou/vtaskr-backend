from typing import Self

from src.tasks.models import Tag, Task

from .tenant_queryset import TenantQueryset


class TagQueryset(TenantQueryset):
    def __init__(self):
        super().__init__(Tag)

    def task(self, task_id: str) -> Self:
        self._query = self._query.where(self.qs_class.tasks.any(Task.id == task_id))
        return self
