from src.libs.dependencies import DependencyInjector
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
    TemplateFabric,
)
from src.notifications.settings import (
    APP_NAME,
    BASE_NOTIFICATION_EVENTS,
    DEFAULT_SMTP_SENDER,
)
from src.settings import APP_NAME as GLOBAL_APP_NAME
from src.settings import EMAIL_LOGO


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
            **context,
        }

    def add_new_contact(self, contact: Contact) -> Contact:
        """Add a new contact and subscribe to all basics notifications"""

        with self.services.persistence.get_session() as session:
            contact = self.contact_manager.create(session=session, contact=contact)

            for name in BASE_NOTIFICATION_EVENTS:
                self.subscription_manager.subscribe(
                    session=session, name=name, type=MessageType.EMAIL, contact=contact
                )

        return contact

    def update_contact(self, contact: Contact) -> Contact:
        """Update informations of an existing contact"""

        with self.services.persistence.get_session() as session:
            return self.contact_manager.update(session=session, contact=contact)

    def delete_contact(self, contact: Contact) -> None:
        """Delete an existing contact"""

        with self.services.persistence.get_session() as session:
            self.contact_manager.delete(session=session, contact=contact)

    def build_messages(self, name: str, context: dict) -> list[AbstractMessage]:
        """Load messages, translate and interpolate them"""

        with self.services.persistence.get_session() as session:
            subscriptions = self.subscription_manager.get_subscriptions_for_event(
                session=session, name=name, targets=context.get("targets", [])
            )

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

    def notify_all(self):
        # Prepare all senders
        for sender_class in AbstractSender.__subclasses__():
            sender = sender_class()

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
