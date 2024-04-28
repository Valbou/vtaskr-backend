from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from .base_port import InjectablePort


class MessageType(Enum):
    EMAIL = "email"
    SMS = "sms"
    TELEGRAM = "telegram"


class AbstractMessage(ABC):
    message_type: MessageType | None = None

    @abstractmethod
    def __init__(
        self, subscriptions: list, template: object | str, context: dict
    ) -> None:
        raise NotImplementedError

    def get_context(self) -> dict:
        return {}


class AbstractSender(ABC):
    handle_message_types: list[MessageType] = []
    messages = []
    compatible_message_classes = []

    def __init__(self) -> None:
        self.messages = []

    def can_handle(self, message: AbstractMessage) -> bool:
        return message.message_type in self.handle_message_types

    def _convert_message(self, message: AbstractMessage) -> Any:
        return message

    def add_message(self, message: AbstractMessage):
        if isinstance(message, tuple(*self.compatible_message_classes)):
            self.messages.append(self._convert_message(message))

    def add_messages(self, messages: list[AbstractMessage]):
        for message in messages:
            self.add_message(message)

    @abstractmethod
    def send(self):
        raise NotImplementedError


class NotificationPort(InjectablePort, ABC):
    @abstractmethod
    def build_message(self, context: dict):
        raise NotImplementedError

    @abstractmethod
    def add_message(self, message: AbstractMessage):
        raise NotImplementedError

    @abstractmethod
    def notify_all(self):
        raise NotImplementedError

    @abstractmethod
    def notify_event(self, sql_service: InjectablePort, event_name: str, context: dict):
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event_name: str, event_type: Enum, tenant_id: str):
        raise NotImplementedError
