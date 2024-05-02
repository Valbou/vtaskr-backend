from abc import ABC, abstractmethod

from src.notifications.models import Subscription
from src.ports import AbstractDBPort


class SubscriptionDBPort(AbstractDBPort, ABC):
    @abstractmethod
    def update(self, subscription: Subscription) -> bool:
        raise NotImplementedError()
