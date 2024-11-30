from unittest import TestCase

from src.notifications.models import (
    BaseEmailContent,
    BaseTelegramContent,
    MessageFabric,
    MessageType,
)


class TestMessageFabric(TestCase):
    def test_get_message_class(self):
        message_class = MessageFabric.get_message_class(message_type=MessageType.EMAIL)
        self.assertEqual(message_class, BaseEmailContent)
        message_class = MessageFabric.get_message_class(
            message_type=MessageType.TELEGRAM
        )
        self.assertEqual(message_class, BaseTelegramContent)
