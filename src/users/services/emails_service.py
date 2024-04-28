from src.libs.dependencies import DependencyInjector
from src.ports import MessageType
from src.settings import APP_NAME, EMAIL_LOGO
from src.users.config import (
    DEFAULT_SENDER,
    LINK_TO_CHANGE_EMAIL,
    LINK_TO_CHANGE_PASSWORD,
    LINK_TO_LOGIN,
    NAME,
)
from src.users.models import RequestChange, User


class EmailService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services

    def get_register_context(self, user: User) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context_register = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/register",
                "to": user.email,
                "subject": _("{APP_NAME} - Registration Success {first_name}").format(
                    first_name=user.first_name, APP_NAME=APP_NAME
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Registration Success {first_name}").format(
                    first_name=user.first_name
                ),
                "content_title": _("Welcome {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _("Welcome to your new app."),
                "paragraph_2": _("As of now, you can login and enjoy !"),
                "call_to_action": _("Enjoy !"),
                "call_to_action_link": LINK_TO_LOGIN,
            }

            return context_register

    def get_login_context(self, user: User, code: str) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context_login = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/login",
                "to": user.email,
                "subject": _("{APP_NAME} - New login with your account").format(
                    APP_NAME=APP_NAME
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("New login with your account"),
                "content_title": _("Hi {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _(
                    "A login attempt was registered, "
                    "if it's not you, please change your password."
                ),
                "paragraph_2": _("To login, please copy/paste the following code:"),
                "code": code,
                "paragraph_3": self._(
                    "This code stay valid only three minutes, after,"
                    "you need to make a new login attempt."
                ),
                "call_to_action": None,
            }

            return context_login

    def get_email_change_old_context(
        self, user: User, request_change: RequestChange
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context_old_email = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_email",
                "to": user.email,
                "subject": _("{APP_NAME} - Change your Email").format(
                    first_name=user.first_name, APP_NAME=APP_NAME
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Change your Email").format(first_name=user.first_name),
                "content_title": _("Hi {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _("You request to change your email account."),
                "paragraph_2": _(
                    "We have sent to you an email, in your new email account."
                ),
                "paragraph_3": _(
                    "Click on the email sent to your new account and"
                    "copy/paste the following code into the form:"
                ),
                "code": request_change.code,
                "paragraph_4": _(
                    "This old email will be remove of your account after proceed."
                ),
                "call_to_action": None,
            }

            return context_old_email

    def get_email_change_new_context(
        self, user: User, new_email: str, sec_hash: str
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            change_email_link = (
                f"{LINK_TO_CHANGE_EMAIL}&hash={sec_hash}&email={new_email}"
                if "?" in LINK_TO_CHANGE_EMAIL
                else f"{LINK_TO_CHANGE_EMAIL}?hash={sec_hash}&email={new_email}"
            )

            context_new_email = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_email",
                "to": user.email,
                "subject": _("{APP_NAME} - Change your Email").format(
                    first_name=user.first_name, APP_NAME=APP_NAME
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Change your Email").format(first_name=user.first_name),
                "content_title": _("Hi {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _("You request to change your email account."),
                "paragraph_2": _(
                    "We sent you an email, to your old email account "
                    "with a code required to complete the process."
                ),
                "paragraph_3": _("Click on the following button/link to proceed"),
                "paragraph_4": (
                    _("This old email will be removed of your account after proceed.")
                    + _("(link available only 3 minutes).")
                ),
                "call_to_action": _("Change now"),
                "call_to_action_link": change_email_link,
            }

            return context_new_email

    def get_password_change_context(self, user: User, sec_hash: str) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            change_password_link = (
                f"{LINK_TO_CHANGE_PASSWORD}&hash={sec_hash}&email={user.email}"
                if "?" in LINK_TO_CHANGE_PASSWORD
                else f"{LINK_TO_CHANGE_PASSWORD}?hash={sec_hash}&email={user.email}"
            )

            context_new_password = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_password",
                "to": user.email,
                "subject": _("{APP_NAME} - Password Change Request").format(
                    first_name=user.first_name, APP_NAME=APP_NAME
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Password Change Request").format(
                    first_name=user.first_name
                ),
                "content_title": _("Hi {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _("You request us to change your account password."),
                "paragraph_2": _("Click on the following button/link to proceed"),
                "paragraph_3": _("(link available only 3 minutes)"),
                "call_to_action": _("Change now"),
                "call_to_action_link": change_password_link,
            }

            return context_new_password
