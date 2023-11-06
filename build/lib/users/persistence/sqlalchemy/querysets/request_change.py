from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import RequestChange

TRequestChangeQueryset = TypeVar(
    "TRequestChangeQueryset", bound="RequestChangeQueryset"
)


class RequestChangeQueryset(Queryset):
    def __init__(self):
        super().__init__(RequestChange)

    def valid_for(self, email: str) -> TRequestChangeQueryset:
        self._query = self._query.where(
            self.qs_class.email == email,
            self.qs_class.created_at > self.qs_class.valid_after(),
        )
        return self

    def last(self) -> TRequestChangeQueryset:
        self._query = self._query.order_by(self.qs_class.created_at.desc()).limit(1)
        return self

    def expired(self) -> TRequestChangeQueryset:
        self._query = self._query.where(
            self.qs_class.created_at < self.qs_class.history_expired_before()
        )
        return self
