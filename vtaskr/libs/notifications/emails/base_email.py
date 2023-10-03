from abc import ABC
from typing import Optional

from vtaskr.libs.notifications.message import AbstractMessage


class AbstractBaseEmailContent(AbstractMessage, ABC):
    from_email: Optional[str] = None
    to: list[str] = []
    subject: str = ""
    text: str = ""
    html: str = ""
    cc: Optional[list[str]] = None
