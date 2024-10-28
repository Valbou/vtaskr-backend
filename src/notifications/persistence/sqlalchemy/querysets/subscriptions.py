from typing import Self

from src.libs.sqlalchemy.queryset import Queryset
from src.notifications.models import Subscription
from src.ports import MessageType


class SubscriptionQueryset(Queryset):
    def __init__(self):
        super().__init__(Subscription)

    def all_event_subscriptions(self, event_name: str, event_type: MessageType) -> Self:
        self._query = self._query.where(
            self.qs_class.event_name == event_name,
            self.qs_class.event_type == event_type,
        )
        return self
