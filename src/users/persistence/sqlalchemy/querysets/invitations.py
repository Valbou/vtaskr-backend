from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Invitation

TInvitationQueryset = TypeVar("TInvitationQueryset", bound="InvitationQueryset")


class InvitationQueryset(Queryset):
    def __init__(self):
        super().__init__(Invitation)

    def expired(self) -> TInvitationQueryset:
        self._query = self._query.where(
            self.qs_class.created_at < self.qs_class.expired_before()
        )
        return self
