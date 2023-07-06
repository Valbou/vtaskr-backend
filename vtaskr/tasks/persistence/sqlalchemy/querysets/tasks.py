from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.tasks.models import Tag, Task


class TaskQueryset(Queryset):
    def __init__(self):
        super().__init__(Task)

    def user(self, user_id: str):
        self._query = self._query.where(self.qs_class.user_id == user_id)
        return self

    def tag(self, tag_id: str):
        self._query = self._query.where(self.qs_class.tags.any(Tag.id == tag_id))
        return self
