import requests

from src.notifications.models import BaseEmailContent, BaseTelegramContent
from src.ports import AbstractMessage, AbstractSender, MessageType
from src.settings import TELEGRAM_BOT

from .smtp_service import MultiSMTPEmail, SMTPEmail


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
