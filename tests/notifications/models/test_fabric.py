from unittest import TestCase

from src.ports import MessageType
from src.notifications.models import MessageFabric, BaseEmailContent, BaseTelegramContent


class TestMessageFabric(TestCase):
    def test_get_message_class(self):
        message_class = MessageFabric.get_message_class(event_type=MessageType.EMAIL)
        self.assertEqual(message_class, BaseEmailContent)
        message_class = MessageFabric.get_message_class(event_type=MessageType.TELEGRAM)
        self.assertEqual(message_class, BaseTelegramContent)
