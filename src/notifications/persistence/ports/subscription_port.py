from abc import ABC, abstractmethod

from src.notifications.models import MessageType, Subscription
from src.ports import AbstractDBPort


class SubscriptionDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, subscription: Subscription) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_subscriptions_for_event(
        self, session, event_name: str, event_type: MessageType
    ) -> list[Subscription]:
        raise NotImplementedError()
