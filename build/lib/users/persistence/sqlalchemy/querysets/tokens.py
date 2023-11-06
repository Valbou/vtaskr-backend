from typing import TypeVar

from sqlalchemy import and_, or_

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Token

TTokenQueryset = TypeVar("TTokenQueryset", bound="TTokenQueryset")


class TokenQueryset(Queryset):
    def __init__(self):
        super().__init__(Token)

    def by_sha(self, sha_token: str) -> TTokenQueryset:
        self._query = self._query.where(self.qs_class.sha_token == sha_token)
        return self

    def expired(self) -> TTokenQueryset:
        self._query = self._query.where(
            or_(
                self.qs_class.last_activity_at < self.qs_class.expired_before(),
                and_(
                    self.qs_class.created_at < self.qs_class.expired_temp_before(),
                    self.qs_class.temp == True,  # noqa: E712
                ),
            )
        )
        return self
