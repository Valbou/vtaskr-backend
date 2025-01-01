from unittest.mock import MagicMock, patch

from src.notifications.managers import AbstractSender
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

        self.notification_service.add_new_contact(contact=contact, contact_id=None)

        self.notification_service.contact_manager.create.assert_called_once()
        call_count = self.notification_service.subscription_manager.subscribe.call_count
        self.assertEqual(call_count, len(BASE_NOTIFICATION_EVENTS))

    def test_add_new_contact_set_id(self):
        contact = Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )
        self.assertNotEqual(contact.id, "contact_123")

        self.notification_service.contact_manager.create = MagicMock(
            return_value=contact
        )
        self.notification_service.subscription_manager.subscribe = MagicMock()

        new_contact = self.notification_service.add_new_contact(
            contact=contact, contact_id="contact_123"
        )

        self.notification_service.contact_manager.create.assert_called_once()
        call_count = self.notification_service.subscription_manager.subscribe.call_count
        self.assertEqual(call_count, len(BASE_NOTIFICATION_EVENTS))
        self.assertEqual(new_contact.id, "contact_123")

    def test_subscribe(self):
        self.notification_service.subscription_manager.subscribe = MagicMock()

        self.notification_service.subscribe(
            contact=None, event_name="", event_type=MessageType.SMS
        )

        self.notification_service.subscription_manager.subscribe.assert_called_once()

    def test_unsubscribe(self):
        self.notification_service.subscription_manager.unsubscribe = MagicMock()

        self.notification_service.unsubscribe(
            contact=None, event_name="", event_type=MessageType.SMS
        )

        self.notification_service.subscription_manager.unsubscribe.assert_called_once()

    def test_update_contact(self):
        contact = Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )
        self.notification_service.contact_manager.update = MagicMock()

        self.notification_service.update_contact(contact=contact)

        self.notification_service.contact_manager.update.assert_called_once()

    def test_delete_contact(self):
        contact = Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )

        sub_manager = self.notification_service.subscription_manager
        sub_manager.delete_all_subscriptions_with_contact = MagicMock()
        self.notification_service.contact_manager.delete_by_id = MagicMock()

        self.notification_service.delete_contact(contact_id=contact.id)

        sub_manager.delete_all_subscriptions_with_contact.assert_called_once()
        self.notification_service.contact_manager.delete_by_id.assert_called_once()

    def test_build_messages(self):
        event = "users:register:user"
        context = {
            "first_name": "first",
            "email": "test@example.com",
            "LINK_TO_LOGIN": "htttp://www.vtaskr.com",
            "targets": ["abc123"],
        }
        self.notification_service._messages.clear()

        sub_manager = self.notification_service.subscription_manager
        sub_manager.get_subscriptions_for_event = MagicMock(
            return_value=[
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
            ]
        )

        sub_manager.get_subscriptions_indexed_by_message_type = MagicMock(
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

        sub_manager.get_subscriptions_for_event.assert_called_once()
        sub_manager.get_subscriptions_indexed_by_message_type.assert_called_once()

        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], AbstractMessage)

        self.assertEqual(len(self.notification_service._messages), 0)

    def test_build_messages_no_subscriptions(self):
        event = "users:register:user"
        context = {
            "first_name": "first",
            "email": "test@example.com",
            "LINK_TO_LOGIN": "htttp://www.vtaskr.com",
            "targets": ["abc123"],
        }
        self.notification_service._messages.clear()

        sub_manager = self.notification_service.subscription_manager
        sub_manager.get_subscriptions_for_event = MagicMock(return_value=[])

        sub_manager.get_subscriptions_indexed_by_message_type = MagicMock()

        with self.app.app_context():
            messages = self.notification_service.build_messages(
                name=event, context=context
            )

        sub_manager.get_subscriptions_for_event.assert_called_once()
        sub_manager.get_subscriptions_indexed_by_message_type.assert_not_called()

        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 0)

    def test_add_messages(self):
        initial = len(self.notification_service._messages)
        messages = ["a", "b", "c"]

        self.notification_service.add_messages(messages)

        final = len(self.notification_service._messages)
        self.assertEqual(final, initial + len(messages))

    def test_get_sender_classes(self):
        total_senders = 0
        for sender in self.notification_service._get_sender_classes():
            self.assertIsInstance(sender, AbstractSender)
            total_senders += 1

        self.assertEqual(total_senders, 2)

    def test_notify_all(self):
        self.notification_service._messages = ["one_message"]

        special_mock = MagicMock()
        special_mock.can_handle = MagicMock(return_value=True)
        special_mock.add_message = MagicMock()
        special_mock.send = MagicMock()

        self.notification_service._get_sender_classes = MagicMock(
            return_value=[special_mock]
        )

        self.notification_service.notify_all()

        special_mock.can_handle.assert_called_once()
        special_mock.add_message.assert_called_once()
        special_mock.send.assert_called_once()

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
