from abc import ABC, abstractmethod

from src.notifications.settings import MessageType


class AbstractMessage(ABC):
    message_type: MessageType | None = None

    @abstractmethod
    def __init__(
        self, subscriptions: list, template: object | str, context: dict
    ) -> None:
        raise NotImplementedError

    def get_context(self) -> dict:
        return {}
