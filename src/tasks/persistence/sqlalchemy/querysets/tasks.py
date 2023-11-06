from src.tasks.models import Tag, Task

from .tenant_queryset import TenantQueryset


class TaskQueryset(TenantQueryset):
    def __init__(self):
        super().__init__(Task)

    def tag(self, tag_id: str):
        self._query = self._query.where(self.qs_class.tags.any(Tag.id == tag_id))
        return self
