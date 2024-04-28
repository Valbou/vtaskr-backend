from abc import ABC, abstractmethod

from src.libs.sqlalchemy.default_port import AbstractPort
from src.notifications.models import Subscription


class AbstractSubscriptionPort(AbstractPort, ABC):
    @abstractmethod
    def update(self, subscription: Subscription) -> bool:
        raise NotImplementedError()
