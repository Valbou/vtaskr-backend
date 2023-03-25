from abc import ABC
from typing import List, Optional


class AbstractBaseEmailContent(ABC):
    logo: str = ""
    subject: str = ""
    from_email: Optional[str] = None
    to: List[str] = []
    text: str = ""
    html: str = ""
    cc: Optional[List[str]] = None
