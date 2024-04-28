from src.ports import AbstractMessage

from .subscription import Subscription
from .template import Template


class BaseEmailContent(AbstractMessage):
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
        super().__init__()

        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.to for s in subscriptions]
        else:
            self.to = subscriptions

        self.sender = template.sender
        self.subject = template.interpolate_subject(context=context)
        self.html = template.interpolate_html(context=context)
        self.text = template.interpolate_text(context=context)


class BaseTelegramContent(AbstractMessage):
    to: list[str] = []
    text: str = ""

    def __init__(
        self, subscriptions: list[Subscription | str], template: Template, context: dict
    ) -> None:
        super().__init__()

        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.to for s in subscriptions]
        else:
            self.to = subscriptions

        self.to = [s.to for s in subscriptions]
        self.text = template.interpolate_text(context=context)
