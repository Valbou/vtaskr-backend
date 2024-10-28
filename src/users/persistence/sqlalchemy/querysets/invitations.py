from typing import Self

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Invitation


class InvitationQueryset(Queryset):
    def __init__(self):
        super().__init__(Invitation)

    def expired(self) -> Self:
        self._query = self._query.where(
            self.qs_class.created_at < self.qs_class.expired_before()
        )
        return self
