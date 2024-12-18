from unittest import TestCase
from unittest.mock import MagicMock

from src.notifications.models import (
    BaseEmailContent,
    BaseEmailTemplate,
    BaseTelegramContent,
    BaseTelegramTemplate,
    Contact,
    MessageFabric,
    MessageType,
    Subscription,
)
from src.notifications.settings import MessageType


class TestMessageFabric(TestCase):
    def _generate_subscription(self, type: MessageType) -> Subscription:
        return Subscription(
            type=type,
            name="name",
            contact_id="contact_123",
            contact=Contact(
                first_name="first",
                last_name="last",
                email="test@example.com",
                telegram="1234",
            ),
        )

    def test_get_message_class_email(self):
        message_class = MessageFabric.get_message_class(message_type=MessageType.EMAIL)
        self.assertEqual(message_class, BaseEmailContent)

    def test_message_class_email_with_substription(self):
        subscription = self._generate_subscription(type=MessageType.EMAIL)
        template = BaseEmailTemplate()
        template.interpolate_subject = MagicMock()
        template.interpolate_content = MagicMock()

        message = BaseEmailContent(
            session=None,
            subscriptions=[subscription],
            template=template,
            context={},
        )

        self.assertIsInstance(message.to, list)
        for t in message.to:
            with self.subTest(t):
                self.assertIsInstance(t, str)
                self.assertEqual(t, "test@example.com")

        template.interpolate_subject.assert_called_once()
        self.assertEqual(template.interpolate_content.call_count, 2)

    def test_get_message_class_telegram(self):
        message_class = MessageFabric.get_message_class(
            message_type=MessageType.TELEGRAM
        )
        self.assertEqual(message_class, BaseTelegramContent)

    def test_message_class_telegram_with_substription(self):
        subscription = self._generate_subscription(type=MessageType.TELEGRAM)
        template = BaseEmailTemplate()
        template.interpolate_subject = MagicMock()
        template.interpolate_content = MagicMock()

        message = BaseTelegramContent(
            session=None,
            subscriptions=[subscription],
            template=template,
            context={},
        )

        self.assertIsInstance(message.to, list)
        for t in message.to:
            with self.subTest(t):
                self.assertIsInstance(t, str)
                self.assertEqual(t, "1234")

        template.interpolate_subject.assert_not_called()
        template.interpolate_content.assert_called_once()
