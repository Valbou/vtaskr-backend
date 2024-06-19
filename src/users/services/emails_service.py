from src.libs.dependencies import DependencyInjector
from src.ports import MessageType
from src.settings import APP_NAME, EMAIL_LOGO
from src.users.models import Group, Invitation, RequestChange, RoleType, User
from src.users.settings import APP_NAME as NAME
from src.users.settings import (
    DEFAULT_SENDER,
    LINK_TO_CHANGE_EMAIL,
    LINK_TO_CHANGE_PASSWORD,
    LINK_TO_JOIN_GROUP,
    LINK_TO_LOGIN,
)


class EmailService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services

    def get_register_context(self, user: User) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/register",
                "email": user.email,
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

            return context

    def get_login_context(self, user: User, code: str) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/login",
                "email": user.email,
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
                "paragraph_3": _(
                    "This code stay valid only three minutes, after,"
                    "you need to make a new login attempt."
                ),
                "call_to_action": None,
            }

            return context

    def get_email_change_old_context(
        self, user: User, request_change: RequestChange
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_email",
                "email": user.email,
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

            return context

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

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_email",
                "email": user.email,
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

            return context

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

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/change_password",
                "email": user.email,
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

            return context

    def get_delete_context(self, user: User) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/delete",
                "email": user.email,
                "subject": _("{APP_NAME} - Account deleted").format(APP_NAME=APP_NAME),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Account deleted"),
                "content_title": _("Hi {first_name} !").format(
                    first_name=user.first_name
                ),
                "paragraph_1": _(
                    "Your account id definitely deleted, "
                    "all associated data are definitely removed."
                ),
                "paragraph_2": _("We hope to see you soon ! Bye !"),
            }

            return context

    def get_invitation_context(
        self, user: User, group: Group, roletype: RoleType, invitation: Invitation
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            join_group_link = (
                f"{LINK_TO_JOIN_GROUP}&hash={invitation.gen_hash()}"
                if "?" in LINK_TO_CHANGE_PASSWORD
                else f"{LINK_TO_CHANGE_PASSWORD}?hash={invitation.gen_hash()}"
            )

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/invitation",
                "email": invitation.to_user_email,
                "subject": _(
                    "{APP_NAME} - Invitation to join group {group_name} as {group_role}"
                ).format(
                    APP_NAME=APP_NAME, group_name=group.name, group_role=roletype.name
                ),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Invitation to group {group_name}").format(
                    group_name=group.name
                ),
                "content_title": _("Hi !"),
                "paragraph_1": _(
                    "You are invited to contribute to the group {group_name} as {group_role}, "
                    "by user {host_first_name}."
                ).format(
                    host_first_name=user.first_name,
                    group_name=group.name,
                    group_role=roletype.name,
                ),
                "paragraph_2": _("Click on the link below to join the group."),
                "paragraph_3": _(
                    "You need to be logged in to accept invitation. "
                    "If necessary register first."
                ),
                "call_to_action": _("Join now"),
                "call_to_action_link": join_group_link,
            }

            return context

    def get_accepted_invitation_context(
        self, user: User, group: Group, roletype: RoleType, host_user: User
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/invitation",
                "email": host_user.email,
                "subject": _(
                    "{APP_NAME} - {first_name} has joined group {group_name} as {group_role}"
                ).format(
                    APP_NAME=APP_NAME, group_name=group.name, group_role=roletype.name
                ),
                "tenant_id": host_user.id,
                "logo": EMAIL_LOGO,
                "title": _("Accepted invitation to group {group_name}"),
                "content_title": _("Hi {host_first_name} !").format(
                    host_first_name=host_user.first_name
                ),
                "paragraph_1": _(
                    "{first_name} accept to contribute to the group {group_name} as {group_role}"
                ).format(
                    first_name=user.first_name,
                    group_name=group.name,
                    group_role=roletype.name,
                ),
            }

            return context

    def get_cancelled_invitation_context(
        self, user: User, group: Group, invitation: Invitation
    ) -> dict:
        with self.services.translation.get_translation_session(
            domain=NAME, locale=user.locale
        ) as trans:
            _ = trans.gettext

            context = {
                "message_type": MessageType.EMAIL,
                "sender": DEFAULT_SENDER,
                "template": "emails/invitation",
                "email": invitation.to_user_email,
                "subject": _(
                    "{APP_NAME} - Invitation to {group_name} cancelled"
                ).format(APP_NAME=APP_NAME, group_name=group.name),
                "tenant_id": user.id,
                "logo": EMAIL_LOGO,
                "title": _("Invitation to group {group_name} cancelled"),
                "content_title": _("Hi !"),
                "paragraph_1": _(
                    "Invitation to group {group_name} was cancelled by {host_first_name}"
                ).format(
                    host_first_name=user.first_name,
                    group_name=group.name,
                ),
            }

            return context
