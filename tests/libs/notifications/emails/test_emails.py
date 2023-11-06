import os
from unittest import TestCase
from unittest.mock import patch

from src.libs.notifications.emails import MultiSMTPEmail, SMTPEmail

DEFAULT_SMTP_SENDER = os.getenv("DEFAULT_SMTP_SENDER")


class TestSMTPEmail(TestCase):
    def _create_email(self) -> SMTPEmail:
        return SMTPEmail(
            from_email=DEFAULT_SMTP_SENDER,
            to_emails=DEFAULT_SMTP_SENDER,
            subject="Test SMTP Email",
            text="Hello World - Test message",
            html="""
            <html>
                <body>
                    <h1>Hello World</h1>
                    <p>Test mesage</p>
                </body
            </html>
            """,
            cc_emails=[DEFAULT_SMTP_SENDER, DEFAULT_SMTP_SENDER],
            bcc_emails=[DEFAULT_SMTP_SENDER],
        )

    def test_email_struct(self):
        email = self._create_email()
        result = email.message.as_string()
        self.assertIn("Subject: Test SMTP Email", result)
        self.assertIn(f"From: {DEFAULT_SMTP_SENDER}", result)
        self.assertIn(f"To: {DEFAULT_SMTP_SENDER}", result)
        self.assertIn(f"Cc: {DEFAULT_SMTP_SENDER}, {DEFAULT_SMTP_SENDER}", result)
        self.assertIn('Content-Type: text/plain; charset="utf-8"', result)
        self.assertIn("Hello World - Test message", result)
        self.assertIn('Content-Type: text/html; charset="utf-8"', result)
        self.assertIn("<h1>Hello World</h1>", result)

    def test_email_sent(self):
        email = self._create_email()
        with patch("smtplib.SMTP_SSL.sendmail") as mock:
            email.send()
            mock.assert_called_once()

    def test_multi_email_sent(self):
        NB_EMAIL = 5
        multi = MultiSMTPEmail()
        self.assertFalse(multi.has_messages)
        for _ in range(NB_EMAIL):
            multi.add_email(self._create_email())
        self.assertTrue(multi.has_messages)
        with patch("smtplib.SMTP_SSL.sendmail") as mock:
            multi.send_all()
            mock.assert_called()
            self.assertEqual(mock.call_count, NB_EMAIL)
