from vtaskr.libs.sqlalchemy.queryset import Queryset
from vtaskr.users.models import Role


class RoleQueryset(Queryset):
    def __init__(self):
        super().__init__(Role)

    def has_right(self, group_id: str, resource: str):
        self._query = self._query.where(self.qs_class.group_id == group_id)

    def last(self):
        self._query = self._query.order_by(self.qs_class.created_at.desc()).limit(1)
        return self

    def expired(self):
        self._query = self._query.where(
            self.qs_class.created_at < self.qs_class.history_expired_before()
        )
        return self
