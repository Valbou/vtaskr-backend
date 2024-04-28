from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.notifications.models import MessageType, Subscription
from src.notifications.persistence.ports import AbstractSubscriptionPort
from src.notifications.persistence.sqlalchemy.querysets import SubscriptionQueryset


class SubscriptionDB(AbstractSubscriptionPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = SubscriptionQueryset()

    def update(
        self, session: Session, subscription: Subscription, autocommit: bool = True
    ) -> bool:
        self.qs.update().id(subscription.id).values(
            to=subscription.to,
            cc=subscription.cc,
            bcc=subscription.bcc,
            event_name=subscription.event_name,
            event_type=subscription.event_type,
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
        )
        session.execute(self.qs.statement)

        if autocommit:
            session.commit()

    def get_subscriptions_for_event(
        self, session: Session, event_name: str, event_type: MessageType
    ) -> list[Subscription]:
        self.qs.all_event_subscriptions(event_name=event_name, event_type=event_type)
        return session.scalars(self.qs.statement).all()
