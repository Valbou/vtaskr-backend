from src.notifications.models import BaseEmailContent
from src.ports import AbstractMessage, AbstractSender, MessageType

from .smtp_service import MultiSMTPEmail, SMTPEmail


class EmailSender(AbstractSender):
    handle_message_types = [MessageType.EMAIL]

    def __init__(self) -> None:
        self.multi_smtp = MultiSMTPEmail()
        self.compatible_message_classes = [BaseEmailContent]

    def _convert_message(self, message: AbstractMessage) -> SMTPEmail:
        return SMTPEmail.from_base_email_content(message)

    def send(self):
        if self.multi_smtp.has_messages:
            self.multi_smtp.send_all()


class TelegramSender(AbstractSender):
    handle_message_types = [MessageType.TELEGRAM]
