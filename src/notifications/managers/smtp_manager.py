import logging
import ssl
from email.message import EmailMessage
from smtplib import SMTP_SSL

from src.notifications.models import BaseEmailContent
from src.notifications.settings import (
    DEFAULT_SMTP_HOST,
    DEFAULT_SMTP_PASS,
    DEFAULT_SMTP_PORT,
    DEFAULT_SMTP_USER,
)

logger = logging.getLogger(__name__)


class NoEmailContentError(Exception):
    pass


def get_smtp_server(
    host: str | None = None,
    port: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> SMTP_SSL:
    ssl_default_context = ssl.create_default_context()
    host = host or DEFAULT_SMTP_HOST
    port = port or DEFAULT_SMTP_PORT
    user = user or DEFAULT_SMTP_USER
    password = password or DEFAULT_SMTP_PASS

    server = SMTP_SSL(host, port, context=ssl_default_context)
    server.login(user, password)
    return server


class SMTPEmail:
    def __init__(
        self,
        from_email: str,
        to_emails: list[str] | str,
        subject: str,
        text: str = "",
        html: str = "",
        cc_emails: list[str] | None = None,
        bcc_emails: list[str] | None = None,
    ) -> None:
        if not text and not html:
            raise NoEmailContentError("Error: Email as no content !")

        self.from_email = from_email
        self.to_emails = to_emails if isinstance(to_emails, str) else ",".join(to_emails)
        self.subject = subject
        self.text = text
        self.html = html
        self.cc_emails = cc_emails or []
        self.bcc_emails = bcc_emails or []
        self._create_email_multipart_alternative()

    def _create_email_multipart_alternative(self) -> EmailMessage:
        self.message = EmailMessage()
        self.message["Subject"] = self.subject
        self.message["From"] = self.from_email
        self.message["To"] = self.to_emails
        self.message["Cc"] = self.cc_emails
        self.message["Bcc"] = self.bcc_emails
        self.message.set_charset("utf-8")

        if self.text:
            self.message.set_content(self.text)
        if self.html:
            self.message.add_alternative(self.html, subtype="html")

    def send(
        self,
        host: str | None = None,
        port: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ):
        server = get_smtp_server(host, port, user, password)
        logger.info(
            f"Send Multi from {self.from_email} "
            f"to {self.to_emails} subject {self.subject}"
        )
        server.sendmail(self.from_email, self.to_emails, self.message.as_string())
        server.quit()

    @classmethod
    def from_base_email_content(
        cls, email: BaseEmailContent, from_email: str | None = None
    ):
        from_email = from_email or DEFAULT_SMTP_USER

        return SMTPEmail(
            from_email=from_email,
            to_emails=email.to,
            subject=email.subject,
            text=email.text,
            html=email.html,
            cc_emails=email.cc,
            bcc_emails=email.bcc,
        )


class MultiSMTPEmail:
    def __init__(self) -> None:
        self.emails: list[SMTPEmail] = []

    def add_email(self, email: SMTPEmail):
        self.emails.append(email)

    def add_emails(self, emails: list[SMTPEmail]):
        self.emails.extend(emails)

    def send_all(
        self,
        host: str | None = None,
        port: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ):
        server = get_smtp_server(host, port, user, password)
        while self.emails:
            email = self.emails.pop()

            logger.info(
                f"Send Multi from {email.from_email} "
                f"to {email.to_emails} subject {email.subject}"
            )
            server.sendmail(email.from_email, email.to_emails, email.message.as_string())

        self.emails.clear()
        server.quit()

    @property
    def has_messages(self):
        return bool(self.emails)
