from abc import ABC
from typing import List, Optional

from vtaskr.notifications.message import AbstractMessage


class AbstractBaseEmailContent(AbstractMessage, ABC):
    from_email: Optional[str] = None
    to: List[str] = []
    subject: str = ""
    text: str = ""
    html: str = ""
    cc: Optional[List[str]] = None
