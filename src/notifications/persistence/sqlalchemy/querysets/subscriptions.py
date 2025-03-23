from typing import Self

from src.libs.sqlalchemy.queryset import Queryset
from src.notifications.models import Subscription


class SubscriptionQueryset(Queryset):
    def __init__(self):
        super().__init__(Subscription)

    def all_events_subscriptions(self, names: list[str], targets: list[str]) -> Self:
        self._query = self._query.where(
            self.qs_class.name.in_(names), self.qs_class.contact_id.in_(targets)
        )

        return self
