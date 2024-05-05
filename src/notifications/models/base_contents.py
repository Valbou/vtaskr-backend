from src.ports import AbstractMessage, MessageType

from .subscription import Subscription
from .template import Template


class BaseEmailContent(AbstractMessage):
    message_type = MessageType.EMAIL
    sender: str | None = None
    to: list[str] = []
    subject: str = ""
    text: str = ""
    html: str = ""
    cc: list[str] | None = None
    bcc: list[str] | None = None

    def __init__(
        self, subscriptions: list[Subscription | str], template: Template, context: dict
    ) -> None:
        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.contact.email for s in subscriptions]
        else:
            self.to = subscriptions

        self.sender = template.sender
        self.subject = template.interpolate_subject(context=context)
        self.html = template.interpolate_html(context=context)
        self.text = template.interpolate_text(context=context)


class BaseTelegramContent(AbstractMessage):
    message_type = MessageType.TELEGRAM
    to: list[str] = []
    text: str = ""

    def __init__(
        self, subscriptions: list[Subscription | str], template: Template, context: dict
    ) -> None:
        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.contact.telegram for s in subscriptions]
        else:
            self.to = subscriptions

        self.text = template.interpolate_text(context=context)
