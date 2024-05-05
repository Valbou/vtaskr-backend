from unittest.mock import MagicMock

from src.notifications.models import BaseEmailContent, Contact
from src.notifications.services import NotificationService
from src.ports import MessageType
from tests.base_test import BaseTestCase


class TestNotificationsService(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.notification_service = NotificationService()
        self.notification_service.set_context(app=self.app)

    def test_build_message(self):
        context = {
            "message_type": MessageType.EMAIL,
            "sender": "Test Sender <sender@example.com>",
            "template": "emails/login",
            "to": "receiver@example.com",
            "subject": "Subject Test {paragraph_1}",
            "tenant_id": "",
            "title": "Title Test",
            "content_title": "Content Title Test",
            "paragraph_1": "p1",
            "paragraph_2": "p2",
            "code": "code",
            "paragraph_3": "p3",
            "call_to_action": None,
        }
        message: BaseEmailContent = self.notification_service.build_message(context)
        self.notification_service.add_message(message=message)

        self.assertIsInstance(message, BaseEmailContent)
        self.assertEqual(len(self.notification_service.messages), 1)
        self.assertEqual(message.subject, "Subject Test p1")

    def test_subscribe(self):
        telegram_chat_id = "a1b2c3d4"
        tenant_id = "abc132"
        contact = Contact(
            id=tenant_id,
            telegram=telegram_chat_id,
        )
        self.notification_service.contact_db.load = MagicMock(return_value=contact)
        self.notification_service.subscription_db = MagicMock()

        subscription = self.notification_service.subscribe(
            event_name="test:subscribe",
            event_type=MessageType.TELEGRAM,
            tenant_id=tenant_id,
        )

        self.notification_service.contact_db.load.assert_called_once()
        self.notification_service.subscription_db.save.assert_called_once()
        self.assertEqual(subscription.contact_id, tenant_id)
        self.assertEqual(subscription.contact.telegram, telegram_chat_id)
        self.assertEqual(subscription.event_type, MessageType.TELEGRAM)
        self.assertEqual(subscription.event_name, "test:subscribe")
