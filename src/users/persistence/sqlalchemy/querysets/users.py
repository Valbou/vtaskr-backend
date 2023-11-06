from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import User

TUserQueryset = TypeVar("TUserQueryset", bound="TUserQueryset")


class UserQueryset(Queryset):
    def __init__(self):
        super().__init__(User)

    def by_email(self, email: str) -> TUserQueryset:
        self._query = self._query.where(self.qs_class.email == email)
        return self

    def unused(self) -> TUserQueryset:
        self._query = self._query.where(
            self.qs_class.last_login_at == None,  # noqa E711
            self.qs_class.created_at < self.qs_class.unused_before(),
        )
        return self
