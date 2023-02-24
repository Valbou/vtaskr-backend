from .message import AbstractMessage
from .emails import SMTPEmail, MultiSMTPEmail, AbstractBaseEmailContent


class NotificationService:
    def __init__(self, testing: bool = False) -> None:
        self.testing = testing
        self.multi_smtp = MultiSMTPEmail()

    def add_message(self, message: AbstractMessage):
        if isinstance(message, AbstractBaseEmailContent):
            self.multi_smtp.add_email(SMTPEmail.from_base_email_content(message))

    def notify_all(self):
        if not self.testing and self.multi_smtp.has_messages:
            self.multi_smtp.send_all()
