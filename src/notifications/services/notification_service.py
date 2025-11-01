from logging import getLogger
from typing import Generator

from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.notifications.events import EVENT_LIST
from src.notifications.managers import (
    AbstractSender,
    ContactManager,
    SubscriptionManager,
)
from src.notifications.models import (
    AbstractMessage,
    Contact,
    MessageFabric,
    MessageType,
    Subscription,
    TemplateFabric,
)
from src.notifications.settings import (
    APP_NAME,
    BASE_NOTIFICATION_EVENTS,
    DEFAULT_SMTP_SENDER,
    LINK_TO_CHANGE_EMAIL,
    LINK_TO_CHANGE_PASSWORD,
    LINK_TO_JOIN_GROUP,
    LINK_TO_LOGIN,
)
from src.settings import APP_NAME as GLOBAL_APP_NAME
from src.settings import EMAIL_LOGO

logger = getLogger(__name__)


class NotificationService:
    _messages: list[AbstractMessage] = []

    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self._define_managers()

    def _define_managers(self):
        """Define managers from domain (no DI here)"""

        self.subscription_manager = SubscriptionManager(services=self.services)
        self.contact_manager = ContactManager(services=self.services)

    def _extend_context(self, context: dict) -> dict:
        return {
            "APP_NAME": GLOBAL_APP_NAME,
            "DEFAULT_SMTP_SENDER": DEFAULT_SMTP_SENDER,
            "EMAIL_LOGO": EMAIL_LOGO,
            "LINK_TO_CHANGE_EMAIL": LINK_TO_CHANGE_EMAIL,
            "LINK_TO_CHANGE_PASSWORD": LINK_TO_CHANGE_PASSWORD,
            "LINK_TO_JOIN_GROUP": LINK_TO_JOIN_GROUP,
            "LINK_TO_LOGIN": LINK_TO_LOGIN,
            **context,
        }

    def add_new_contact(self, contact: Contact, contact_id: str | None) -> Contact:
        """Add a new contact and subscribe to all basics notifications"""

        if contact_id is not None:
            contact.id = contact_id

        with self.services.persistence.get_session() as session:
            contact = self.contact_manager.create(session=session, contact=contact)

            for name in BASE_NOTIFICATION_EVENTS:
                self.subscription_manager.subscribe(
                    session=session, name=name, type=MessageType.EMAIL, contact=contact
                )

        return contact

    def get_contact_from_email(self, email: str) -> Contact | None:
        """Return a contact from an email if exists"""

        with self.services.persistence.get_session() as session:
            return self.contact_manager.get_by_email(session, email)

    def subscribe(
        self, contact: Contact, event_name: str, event_type: MessageType
    ) -> None:
        """Subscribe to an event notification"""

        with self.services.persistence.get_session() as session:
            self.subscription_manager.subscribe(
                session=session, name=event_name, type=event_type, contact=contact
            )

    def create_new_contact_subscription(
        self, user_id: str, subscription: Subscription
    ) -> bool:
        """Create user contact subscription"""

        if user_id == subscription.contact_id and subscription.name in EVENT_LIST:
            with self.services.persistence.get_session() as session:
                return self.subscription_manager.register_subscription(
                    session=session, subscription=subscription
                )

        return False

    def unsubscribe(
        self, contact: Contact, event_name: str, event_type: MessageType
    ) -> None:
        """Unsubscribe to an event notification"""

        with self.services.persistence.get_session() as session:
            self.subscription_manager.unsubscribe(
                session=session, name=event_name, type=event_type, contact=contact
            )

    def get_all_contact_subscriptions(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Subscription]:
        """Return all events a user can manage"""

        with self.services.persistence.get_session() as session:
            self.subscription_manager.get_contact_subscriptions_for_event(
                session=session,
                user_id=user_id,
                public_events=EVENT_LIST,
                filters=qs_filters,
            )

    def update_contact(self, contact: Contact) -> Contact:
        """Update informations of an existing contact"""

        with self.services.persistence.get_session() as session:
            return self.contact_manager.update(session=session, contact=contact)

    def delete_contact(self, contact_id: str) -> None:
        """Delete an existing contact"""

        with self.services.persistence.get_session() as session:
            self.subscription_manager.delete_all_subscriptions_with_contact(
                session=session, contact_id=contact_id
            )
            self.contact_manager.delete_by_id(session=session, contact_id=contact_id)

    def build_messages(self, name: str, context: dict) -> list[AbstractMessage]:
        """Load messages, translate and interpolate them"""

        targets = context["targets"]
        with self.services.persistence.get_session() as session:
            subscriptions = self.subscription_manager.get_subscriptions_for_event(
                session=session, name=name, targets=targets
            )

        if len(subscriptions) == 0:
            logger.error(f"No subscription found for event {name} and targets {targets}")
            return []

        indexed_subscriptions = (
            self.subscription_manager.get_subscriptions_indexed_by_message_type(
                subscriptions=subscriptions
            )
        )

        context = self._extend_context(context=context)

        messages = []
        fab = TemplateFabric()
        for sub_type_name, subs in indexed_subscriptions.items():
            sub_type = [m for m in MessageType if m.name == sub_type_name][0]
            template = fab.get_template(template_type=sub_type, name=name)

            for sub in subs:
                with self.services.translation.get_translation_session(
                    domain=APP_NAME, locale=sub.contact.locale
                ) as trans_session:
                    message_class = MessageFabric.get_message_class(
                        message_type=sub_type
                    )
                    messages.append(
                        message_class(
                            session=trans_session,
                            subscriptions=subs,
                            template=template,
                            context=context,
                        )
                    )

            return messages

    def add_messages(self, messages: list[AbstractMessage]):
        self._messages.extend(messages)

    def _get_sender_classes(self) -> Generator[AbstractSender, None, None]:
        for sender_class in AbstractSender.__subclasses__():
            yield sender_class()

    def notify_all(self):
        # Prepare all senders
        for sender in self._get_sender_classes():

            # Dispatch messages
            for message in self._messages:
                if sender.can_handle(message):
                    sender.add_message(message)

            # Fire all messages stored in sender
            sender.send()

        # Flush all messages
        self._messages.clear()

    def notify(self, event_name: str, event_data: dict):
        messages = self.build_messages(name=event_name, event_data=event_data)
        self.add_messages(messages=messages)
        self.notify_all()
