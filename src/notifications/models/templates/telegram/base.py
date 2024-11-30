from src.notifications.settings import MessageType

from ..abstract import AbstractTemplate


class BaseTelegramTemplate(AbstractTemplate):
    event_type: MessageType = MessageType.TELEGRAM
    event_name: str = ""
