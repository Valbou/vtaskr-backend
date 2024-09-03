from unittest.mock import MagicMock, patch

from src.notifications.models import (
    BaseEmailContent,
    BaseTelegramContent,
    MessageType,
    Template,
)
from src.notifications.services import SMTPEmail
from src.notifications.services.senders import EmailSender, TelegramSender
from tests.base_test import DummyBaseTestCase


class BaseSenderTest(DummyBaseTestCase):
    def setUp(self, message_type: MessageType) -> None:
        super().setUp()

        self.template = Template(
            event_type=message_type,
            event_name="Test",
            sender="My Sender",
            name="My Name",
            subject="Test Subject",
            html="template_html",
            text="template_txt",
        )
        self.template.interpolate_html = MagicMock(return_value="Interpolated html")
        self.template.interpolate_text = MagicMock(return_value="Interpolated text")
        self.template.interpolate_subject = MagicMock(
            return_value="Interpolated subject"
        )


class TestEmailSender(BaseSenderTest):
    def setUp(self) -> None:
        super().setUp(message_type=MessageType.EMAIL)

        self.email_sender = EmailSender()
        self.message = BaseEmailContent(
            subscriptions="test@example.com",
            template=self.template,
            context={"hello": "world"},
        )

    def test_convert_message(self):
        converted_message = self.email_sender._convert_message(message=self.message)
        self.assertIsNotNone(converted_message)
        self.assertIsInstance(converted_message, SMTPEmail)

    def test_add_message(self):
        self.assertEqual(len(self.email_sender.messages), 0)

        self.email_sender.add_message(message=self.message)
        self.assertEqual(len(self.email_sender.messages), 1)

        self.email_sender.add_messages(messages=[self.message, self.message])
        self.assertEqual(len(self.email_sender.messages), 3)

        self.email_sender.messages.clear()

    def test_send(self):
        self.email_sender.multi_smtp.send_all = MagicMock()

        self.email_sender.add_message(message=self.message)
        self.assertEqual(len(self.email_sender.messages), 1)

        self.email_sender.send()
        self.assertEqual(len(self.email_sender.messages), 0)

        self.email_sender.multi_smtp.send_all.assert_called_once()


class TestTelegramSender(BaseSenderTest):
    def setUp(self) -> None:
        super().setUp(message_type=MessageType.TELEGRAM)

        self.telegram_sender = TelegramSender()
        self.message = BaseTelegramContent(
            subscriptions="test@example.com",
            template=self.template,
            context={"hello": "world"},
        )

    def test_add_message(self):
        self.assertEqual(len(self.telegram_sender.messages), 0)

        self.telegram_sender.add_message(message=self.message)
        self.assertEqual(len(self.telegram_sender.messages), 1)

        self.telegram_sender.add_messages(messages=[self.message, self.message])
        self.assertEqual(len(self.telegram_sender.messages), 3)

        self.telegram_sender.messages.clear()

    def test_send(self):
        self.telegram_sender.add_message(message=self.message)
        self.assertEqual(len(self.telegram_sender.messages), 1)

        with patch("requests.post") as mock:
            self.telegram_sender.send()
            mock.assert_called_once()

        self.assertEqual(len(self.telegram_sender.messages), 0)
