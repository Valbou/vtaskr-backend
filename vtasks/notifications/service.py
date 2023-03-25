from typing import List

from .emails import SMTPEmail


class NotificationService:
    def __init__(self, testing: bool = False) -> None:
        self.testing = testing

    def notify_by_email(
        self,
        from_email,
        to_emails: List[str],
        subject: str,
        text: str = "",
        html: str = "",
    ):
        email = SMTPEmail(from_email, to_emails, subject, text, html)
        if not self.testing:
            email.send()
