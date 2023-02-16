import ssl
import os

from typing import List, Optional, Union
from smtplib import SMTP_SSL
from email.message import EmailMessage


class NoEmailContentError(Exception):
    pass


def get_smtp_server(
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> SMTP_SSL:
    ssl_default_context = ssl.create_default_context()
    host = host or os.getenv("DEFAULT_SMTP_HOST")
    port = port or os.getenv("DEFAULT_SMTP_PORT")
    user = user or os.getenv("DEFAULT_SMTP_USER")
    password = password or os.getenv("DEFAULT_SMTP_PASS")

    server = SMTP_SSL(host, port, context=ssl_default_context)
    server.login(user, password)
    return server


class SMTPEmail:
    def __init__(
        self,
        from_email: str,
        to_emails: Union[List[str], str],
        subject: str,
        text: str = "",
        html: str = "",
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
    ) -> None:
        if not text and not html:
            raise NoEmailContentError("Error: Email as no content !")

        self.from_email = from_email
        self.to_emails = (
            to_emails if isinstance(to_emails, str) else ",".join(to_emails)
        )
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
        host: Optional[str] = None,
        port: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        server = get_smtp_server(host, port, user, password)
        server.sendmail(self.from_email, self.to_emails, self.message.as_string())
        server.quit()


class MultiSMTPEmail:
    def __init__(self) -> None:
        self.emails = []

    def add_email(self, email: SMTPEmail):
        self.emails.append(email)

    def send_all(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        server = get_smtp_server(host, port, user, password)
        for email in self.emails:
            server.sendmail(
                email.from_email, email.to_emails, email.message.as_string()
            )
        server.quit()
