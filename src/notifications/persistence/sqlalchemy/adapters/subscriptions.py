from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.notifications.models import Subscription
from src.notifications.persistence.ports import SubscriptionDBPort
from src.notifications.persistence.sqlalchemy.querysets import SubscriptionQueryset
from src.notifications.settings import MessageType


class SubscriptionDB(SubscriptionDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = SubscriptionQueryset()

    def update(self, session: Session, subscription: Subscription) -> bool:
        self.qs.update().id(subscription.id).values(
            name=subscription.name,
            type=subscription.type,
        )
        session.execute(self.qs.statement)

    def get_subscriptions_for_event(
        self, session: Session, name: str, targets: list[str]
    ) -> list[Subscription]:
        self.qs.select().all_event_subscriptions(name=name, targets=targets)

        return session.scalars(self.qs.statement).all()

    def delete_with_contact(
        self, session: Session, name: str, type: MessageType, contact_id: str
    ) -> None:
        self.qs.delete().where(
            Subscription.contact_id == contact_id,
            Subscription.name == name,
            Subscription.type == type,
        )
        session.execute(self.qs.statement)

    def delete_all_with_contact(self, session: Session, contact_id: str) -> None:
        self.qs.delete().where(Subscription.contact_id == contact_id)
        session.execute(self.qs.statement)
