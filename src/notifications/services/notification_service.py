from src.notifications.models import MessageFabric, Subscription, Template
from src.notifications.persistence.sqlalchemy.adapters import SubscriptionDB, TemplateDB
from src.ports import AbstractMessage, AbstractSender, MessageType, NotificationPort


class NotificationService(NotificationPort):
    messages: list[AbstractMessage] = []

    def __init__(self) -> None:
        self.subscription_db = SubscriptionDB()
        self.template_db = TemplateDB()
        self.messages = []

    def set_context(self, **ctx) -> None:
        self.app = ctx.pop("app")

    def build_message(self, context: dict) -> AbstractMessage:
        message_type = context.pop("message_type")
        template = Template.temp_template_from_context(context=context)
        subscription = Subscription.temp_template_from_context(context=context)

        return MessageFabric.get_base_message_class(event_type=message_type)(
            subscriptions=[subscription], template=template, context=context
        )

    def add_message(self, message: AbstractMessage):
        self.messages.append(message)

    def notify_all(self):
        # Prepare all senders
        for sender_class in AbstractSender.__subclasses__():
            sender = sender_class()

            # Dispatch messages
            for message in self.messages:
                if sender.can_handle(message):
                    sender.add_message(message)

            # Fire all messages stored in sender
            sender.send()

        # Flush all messages
        self.messages.clear()

    def notify_event(self, event_name: str, context: dict):
        with self.app.dependencies.persistence.get_session() as session:
            for event_type in MessageType:
                subscriptions = self.subscription_db.get_subscriptions_for_event(
                    session=session, event_name=event_name, event_type=event_type
                )

                if subscriptions:
                    template = self.template_db.get_template_for_event(
                        session=session, event_name=event_name, event_type=event_type
                    )

                    if template:
                        message = MessageFabric.get_base_message_class(
                            event_type=event_type
                        )(
                            subscriptions=subscriptions,
                            template=template,
                            context=context,
                        )

                        self.add_notification(message)

            self.notify_all()

    def subscribe(
        self, event_name: str, event_type: MessageType, tenant_id: str, to: str
    ):
        subscription = Subscription(
            event_type=event_type,
            event_name=event_name,
            tenant_id=tenant_id,
            to=to,
        )

        with self.app.dependencies.persistence.get_session() as session:
            self.subscription_db.save(session, subscription)


class TestNotificationService(NotificationService):
    def notify_all(self):
        """No send in test environnement"""
        pass

    def notify_event(self, event_name: str, context: dict):
        """No send in test environnement"""
        pass
