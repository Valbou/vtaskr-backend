from src.notifications.settings import MessageType

from ..subscription import Subscription
from ..templates import BaseEmailTemplate, BaseTelegramTemplate
from .abstract import AbstractMessage


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
        self,
        session,
        subscriptions: list[Subscription | str],
        template: BaseEmailTemplate,
        context: dict,
    ) -> None:
        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.contact.email for s in subscriptions]
        else:
            self.to = subscriptions

        self.sender = template.sender
        self.subject = template.interpolate_subject(session=session, data=context)
        self.html = template.interpolate_content(
            session=session, format="html", data=context
        )
        self.text = template.interpolate_content(
            session=session, format="txt", data=context
        )


class BaseTelegramContent(AbstractMessage):
    message_type = MessageType.TELEGRAM
    to: list[str] = []
    text: str = ""

    def __init__(
        self,
        session,
        subscriptions: list[Subscription | str],
        template: BaseTelegramTemplate,
        context: dict,
    ) -> None:
        if subscriptions and isinstance(subscriptions[0], Subscription):
            self.to = [s.contact.telegram for s in subscriptions]
        else:
            self.to = subscriptions

        self.text = template.interpolate_content(
            session=session, format="txt", data=context
        )
