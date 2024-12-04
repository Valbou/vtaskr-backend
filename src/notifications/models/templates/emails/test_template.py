from gettext import NullTranslations

from .base import BaseEmailTemplate

_ = NullTranslations().gettext


class NotificationsTestTemplate(BaseEmailTemplate):
    """Notification test email template"""

    name: str = _("Test")
    event_name: str = "notifications:test:message"
    subject: str = _("{APP_NAME} - Test Email Notification")
    files_path: dict[str:str] = {
        "html": "emails/notifications/test.html",
        "txt": "emails/notifications/test.txt",
    }

    context = {
        "logo": "{EMAIL_LOGO}",
        "title": _("Test Email Notification"),
        "content_title": _("Hello !"),
        "paragraph_1": _("Email notification works !"),
    }
