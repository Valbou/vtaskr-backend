import os

from .emails import SMTPEmail, AbstractBaseEmailContent


class NotificationService:
    def __init__(self, testing: bool = False) -> None:
        self.testing = testing

    def notify_by_email(
        self,
        email: AbstractBaseEmailContent,
    ):
        from_email = email.from_email or os.getenv("DEFAULT_SMTP_USER")
        email = SMTPEmail(
            from_email,
            email.to,
            email.subject,
            email.text,
            email.html,
            email.cc,
        )
        if not self.testing:
            email.send()
