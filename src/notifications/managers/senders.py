from abc import ABC, abstractmethod

import requests

from src.notifications.managers.smtp_manager import MultiSMTPEmail, SMTPEmail
from src.notifications.models.messages import (
    AbstractMessage,
    BaseEmailContent,
    BaseTelegramContent,
)
from src.notifications.settings import MessageType
from src.settings import TELEGRAM_BOT


class AbstractSender(ABC):
    handle_message_types: list[MessageType] = []
    messages: list[AbstractMessage] = []
    compatible_message_classes: list = []

    def __init__(self) -> None:
        self.messages = []

    def can_handle(self, message: AbstractMessage) -> bool:
        return message.message_type in self.handle_message_types

    def _convert_message(self, message: AbstractMessage) -> AbstractMessage:
        return message

    def add_message(self, message: AbstractMessage):
        if isinstance(message, *self.compatible_message_classes):
            self.messages.append(self._convert_message(message))

    def add_messages(self, messages: list[AbstractMessage]):
        for message in messages:
            self.add_message(message)

    @abstractmethod
    def send(self):
        raise NotImplementedError


class EmailSender(AbstractSender):
    handle_message_types = [MessageType.EMAIL]

    def __init__(self) -> None:
        self.multi_smtp = MultiSMTPEmail()
        self.compatible_message_classes = [BaseEmailContent]

    def _convert_message(self, message: AbstractMessage) -> SMTPEmail:
        return SMTPEmail.from_base_email_content(message)

    def send(self):
        self.multi_smtp.add_emails(emails=self.messages)

        if self.multi_smtp.has_messages:
            self.multi_smtp.send_all()

        self.messages.clear()


class TelegramSender(AbstractSender):
    handle_message_types = [MessageType.TELEGRAM]

    def __init__(self) -> None:
        self.compatible_message_classes = [BaseTelegramContent]

    def send(self):
        for message in self.messages:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"

            for to in message.to.split(","):
                data = {"chat_id": to, "text": message.text}
                requests.post(url, data, timeout=10)

        self.messages.clear()
