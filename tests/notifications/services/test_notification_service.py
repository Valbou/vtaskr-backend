from unittest.mock import MagicMock

from src.notifications.models import AbstractMessage, Contact, Subscription
from src.notifications.services import NotificationService
from src.notifications.settings import BASE_NOTIFICATION_EVENTS, MessageType
from tests.base_test import BaseTestCase


class TestNotificationsService(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.notification_service = NotificationService(services=self.app.dependencies)

    def test_add_new_contact(self):
        contact = Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )

        self.notification_service.contact_manager.create = MagicMock(
            return_value=contact
        )
        self.notification_service.subscription_manager.subscribe = MagicMock()

        self.notification_service.add_new_contact(contact=contact)

        self.notification_service.contact_manager.create.assert_called_once()
        call_count = self.notification_service.subscription_manager.subscribe.call_count
        self.assertEqual(call_count, len(BASE_NOTIFICATION_EVENTS))

    def test_build_messages(self):
        event = "users:register:user"
        context = {
            "first_name": "first",
            "email": "test@example.com",
            "LINK_TO_LOGIN": "htttp://www.vtaskr.com",
            "targets": ["test@example.com"],
        }
        self.notification_service._messages.clear()

        self.notification_service.subscription_manager.get_subscriptions_for_event = (
            MagicMock()
        )
        self.notification_service.subscription_manager.get_subscriptions_indexed_by_message_type = MagicMock(
            return_value={
                MessageType.EMAIL.name: [
                    Subscription(
                        type=MessageType.EMAIL,
                        contact_id="abc123",
                        contact=Contact(
                            first_name="first",
                            last_name="last",
                            email="test@example.com",
                            id="abc132",
                            locale="en_GB",
                        ),
                        name="users:register:user",
                    )
                ],
            }
        )

        with self.app.app_context():
            messages = self.notification_service.build_messages(
                name=event, context=context
            )

        self.notification_service.subscription_manager.get_subscriptions_for_event.assert_called_once()
        self.notification_service.subscription_manager.get_subscriptions_indexed_by_message_type.assert_called_once()

        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], AbstractMessage)

        self.assertEqual(len(self.notification_service._messages), 0)

    def test_add_messages(self):
        initial = len(self.notification_service._messages)
        messages = ["a", "b", "c"]

        self.notification_service.add_messages(messages)

        final = len(self.notification_service._messages)
        self.assertEqual(final, initial + len(messages))

    def test_notify(self):
        event = "users:register:user"
        context = {}

        self.notification_service.build_messages = MagicMock()
        self.notification_service.add_messages = MagicMock()
        self.notification_service.notify_all = MagicMock()

        self.notification_service.notify(event_name=event, event_data=context)

        self.notification_service.build_messages.assert_called_once()
        self.notification_service.add_messages.assert_called_once()
        self.notification_service.notify_all.assert_called_once()
