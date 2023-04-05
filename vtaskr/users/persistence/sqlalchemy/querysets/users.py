from typing import List

from vtaskr.sqlalchemy.queryset import Queryset
from vtaskr.users.models import User


class UserQueryset(Queryset):
    def __init__(self):
        super().__init__(User)

    def user(self, user_id: str):
        self._query = self._query.where(self.qs_class.id == user_id)
        return self

    def users(self, user_ids: List[str]):
        self._query = self._query.where(self.qs_class.in_(user_ids))
        return self

    def with_email(self, email: str):
        self._query = self._query.where(self.qs_class.email == email)
        return self

    def unused(self):
        self._query = self._query.where(
            self.qs_class.last_login_at == None,  # noqa E711
            self.qs_class.created_at < self.qs_class.unused_before(),
        )
        return self
