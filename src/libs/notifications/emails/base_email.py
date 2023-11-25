from abc import ABC

from src.libs.notifications.message import AbstractMessage


class AbstractBaseEmailContent(AbstractMessage, ABC):
    from_email: str | None = None
    to_emails: list[str] = []
    subject: str = ""
    text: str = ""
    html: str = ""
    cc: list[str] | None = None
