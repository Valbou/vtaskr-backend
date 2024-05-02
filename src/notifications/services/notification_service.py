from src.libs.dependencies import DependencyInjector
from src.notifications.models import MessageFabric, Subscription, Template
from src.notifications.persistence import SubscriptionDBPort, TemplateDBPort
from src.notifications.settings import APP_NAME
from src.ports import AbstractMessage, AbstractSender, MessageType, NotificationPort


class NotificationService(NotificationPort):
    messages: list[AbstractMessage] = []

    def __init__(self, **kwargs) -> None:
        self.messages = []

    def set_context(self, **ctx) -> None:
        self.app = ctx.pop("app")
        self.services: DependencyInjector = self.app.dependencies

        self.subscription_db: SubscriptionDBPort = (
            self.services.persistence.get_repository(APP_NAME, "Subscription")
        )
        self.template_db: TemplateDBPort = self.services.persistence.get_repository(
            APP_NAME, "Subscription"
        )

    def build_message(self, context: dict) -> AbstractMessage:
        message_type = context.pop("message_type")
        template = Template.temp_template_from_context(context=context)
        subscription = Subscription.temp_subscription_from_context(context=context)

        with self.app.app_context():
            message_class = MessageFabric.get_message_class(event_type=message_type)
            message = message_class(
                subscriptions=[subscription], template=template, context=context
            )
            return message

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
                        with self.app.app_context():
                            message_class = MessageFabric.get_message_class(
                                event_type=event_type
                            )
                            message = message_class(
                                subscriptions=subscriptions,
                                template=template,
                                context=context,
                            )

                            self.add_message(message)

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
            session.commit()


class TestNotificationService(NotificationService):
    def notify_all(self):
        """No send in test environnement"""
        pass

    def notify_event(self, event_name: str, context: dict):
        """No send in test environnement"""
        pass
