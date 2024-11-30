from src.notifications.settings import DEFAULT_SMTP_SENDER, MessageType

from ..abstract import AbstractTemplate


class BaseEmailTemplate(AbstractTemplate):
    """Base for template creation"""

    event_type: MessageType = MessageType.EMAIL
    event_name: str = ""
    sender: str = DEFAULT_SMTP_SENDER
    files_path: dict[str:str] = {"html": "", "txt": ""}
