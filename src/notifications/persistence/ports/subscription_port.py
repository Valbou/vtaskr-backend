from abc import ABC, abstractmethod

from src.notifications.models import Subscription
from src.ports import AbstractDBPort


class SubscriptionDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, session, subscription: Subscription) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_subscriptions_for_event(
        self, session, name: str, targets: list[str]
    ) -> list[Subscription]:
        raise NotImplementedError()
