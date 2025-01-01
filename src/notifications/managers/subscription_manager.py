from src.libs.dependencies import DependencyInjector
from src.notifications.models import Contact, Subscription
from src.notifications.persistence import SubscriptionDBPort
from src.notifications.settings import APP_NAME, MessageType


class SubscriptionManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.subscription_db: SubscriptionDBPort = (
            self.services.persistence.get_repository(APP_NAME, "Subscription")
        )

    def subscribe(self, session, name: str, type: MessageType, contact: Contact) -> None:
        subscription = Subscription(
            type=type,
            name=name,
            contact_id=contact.id,
            contact=contact,
        )
        self.subscription_db.save(session=session, obj=subscription)

    def unsubscribe(self, session, name: str, type: MessageType, contact_id: str):
        self.subscription_db.delete_with_contact(
            session=session, name=name, type=type, contact_id=contact_id
        )

    def delete_all_subscriptions_with_contact(self, session, contact_id: str) -> None:
        self.subscription_db.delete_all_with_contact(
            session=session, contact_id=contact_id
        )

    def create(self, session, subscription: Subscription) -> None:
        self.subscription_db.save(session=session, obj=subscription)

    def get_subscriptions_indexed_by_message_type(
        self, subscriptions: list[Subscription]
    ) -> dict[MessageType, list[Subscription]]:
        """Index subscription to group by message type"""

        index = {}
        for sub in subscriptions:
            if not index.get(sub.type.name):
                index[sub.type.name] = []

            index[sub.type.name].append(sub)

        return index

    def get_subscriptions_for_event(
        self, session, name: str, targets: list[str]
    ) -> list[Subscription]:
        subscriptions = self.subscription_db.get_subscriptions_for_event(
            session=session, name=name, targets=targets
        )
        return subscriptions
