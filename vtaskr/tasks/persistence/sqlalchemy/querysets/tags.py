from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.tasks.models import Tag, Task


class TagQueryset(Queryset):
    def __init__(self):
        super().__init__(Tag)

    def user(self, user_id: str):
        self._query = self._query.where(self.qs_class.user_id == user_id)
        return self

    def task(self, task_id: str):
        self._query = self._query.where(self.qs_class.tasks.any(Task.id == task_id))
        return self
