from gettext import NullTranslations

from .base import BaseEmailTemplate

_ = NullTranslations().gettext


class UsersRegisterTemplate(BaseEmailTemplate):
    """User register email template"""

    name: str = _("User Register")
    event_name: str = "users:register:user"
    subject: str = _("{APP_NAME} - Registration Success {first_name}")
    files_path: dict[str:str] = {
        "html": "emails/users/register.html",
        "txt": "emails/users/register.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Registration Success {first_name}"),
        "content_title": _("Welcome {first_name} !"),
        "paragraph_1": _("Welcome to your new app."),
        "paragraph_2": _("As of now, you can login and enjoy !"),
        "call_to_action": _("Enjoy !"),
        "call_to_action_link": "{LINK_TO_LOGIN}",
    }


class UsersLogin2FATemplate(BaseEmailTemplate):
    """User 2FA login email template"""

    name: str = _("User 2FA Login")
    event_name: str = "users:login_2fa:user"
    subject: str = _("{APP_NAME} - New login attempt with your account")
    files_path: dict[str:str] = {
        "html": "emails/users/login_2fa.html",
        "txt": "emails/users/login_2fa.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("New login with your account"),
        "content_title": _("Hi {first_name} !"),
        "paragraph_1": _(
            "A login attempt was registered, "
            "if it's not you, please change your password."
        ),
        "paragraph_2": _("To login, please copy/paste the following code:"),
        "code": "{code}",
        "paragraph_3": _(
            "This code stay valid only three minutes, after, "
            "you need to make a new login attempt."
        ),
        "call_to_action": "",
    }


class UsersEmailChangeTemplate(BaseEmailTemplate):
    """User email change email template"""

    name: str = _("User Old Email Change")
    event_name: str = "users:change_email_old:user"
    subject: str = _("{APP_NAME} - Email Change")
    files_path: dict[str:str] = {
        "html": "emails/users/change_email.html",
        "txt": "emails/users/change_email.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Change your Email"),
        "content_title": _("Hi {first_name} !"),
        "paragraph_1": _("You request to change your email account."),
        "paragraph_2": _("We have sent to you an email, in your new email account."),
        "paragraph_3": _(
            "Click on the email sent to your new account and "
            "copy/paste the following code into the form:"
        ),
        "code": "{code}",
        "paragraph_4": _("This old email will be remove of your account after proceed."),
        "call_to_action": "",
    }


class UsersEmailChangeNewTemplate(BaseEmailTemplate):
    """User new email change email template"""

    name: str = _("User New Email Change")
    event_name: str = "users:change_email_new:user"
    subject: str = "{APP_NAME} - Email Change"
    files_path: dict[str:str] = {
        "html": "emails/users/change_email.html",
        "txt": "emails/users/change_email.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "paragraph_1": _("You request to change your email account."),
        "paragraph_2": _(
            "We have sent you an email, to your old email account "
            "with a code required to complete the process."
        ),
        "paragraph_3": _("Click on the following button/link to proceed"),
        "paragraph_4": _(
            "This old email will be removed of your account after proceed."
            " (link available only 3 minutes)."
        ),
        "call_to_action": _("Change now"),
        "call_to_action_link": "{LINK_TO_CHANGE_EMAIL}?hash={hash}&email={new_email}",
    }


class UsersPasswordChangeTemplate(BaseEmailTemplate):
    """User password change template"""

    name: str = _("User Password Change")
    event_name: str = "users:change_password:user"
    subject: str = _("{APP_NAME} - Password Change Request")
    files_path: dict[str:str] = {
        "html": "emails/users/change_password.html",
        "txt": "emails/users/change_password.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Password Change Request"),
        "content_title": _("Hi {first_name} !"),
        "paragraph_1": _("You request us to change your account password."),
        "paragraph_2": _("Click on the following button/link to proceed"),
        "paragraph_3": _("(link available only 3 minutes)"),
        "call_to_action": _("Change now"),
        "call_to_action_link": "{LINK_TO_CHANGE_PASSWORD}?hash={hash}&email={email}",
    }


class UsersDeleteAccountTemplate(BaseEmailTemplate):
    """User delete account template"""

    name: str = _("User Password Change")
    event_name: str = "users:delete:user"
    subject: str = _("{APP_NAME} - Account deleted")
    files_path: dict[str:str] = {
        "html": "emails/users/delete.html",
        "txt": "emails/users/delete.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Account deleted"),
        "content_title": _("Hi {first_name} !"),
        "paragraph_1": _(
            "Your account id definitely deleted, "
            "all associated data are definitely removed."
        ),
        "paragraph_2": _("We hope to see you soon ! Bye !"),
    }


class UsersInvitationTemplate(BaseEmailTemplate):
    """User invitation template"""

    name: str = _("User Invitation")
    event_name: str = "users:invite:user"
    subject: str = _("{APP_NAME} - Invitation to join group {group_name} as {role_name}")
    files_path: dict[str:str] = {
        "html": "emails/users/invitation.html",
        "txt": "emails/users/invitation.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Invitation to group {group_name}"),
        "content_title": _("Hi !"),
        "paragraph_1": _(
            "You are invited to contribute to the group {group_name} as {role_name}, "
            "by user {from_first_name}."
        ),
        "paragraph_2": _("Click on the link below to join the group."),
        "paragraph_3": _(
            "You need to be logged in to accept invitation. "
            "If necessary register first."
        ),
        "call_to_action": _("Join now"),
        "call_to_action_link": "{LINK_TO_CHANGE_PASSWORD}?hash={hash}",
    }


class UsersAcceptedInvitationTemplate(BaseEmailTemplate):
    """User accept invitation template"""

    name: str = "User Accepted Invitation"
    event_name: str = "users:accepted:invitation"
    subject: str = (
        "{APP_NAME} - {to_first_name} has joined group {group_name} as {role_name}"
    )
    files_path: dict[str:str] = {
        "html": "emails/users/invitation.html",
        "txt": "emails/users/invitation.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Accepted invitation to group {group_name}"),
        "content_title": _("Hi {from_first_name} !"),
        "paragraph_1": _(
            "{to_first_name} accept to contribute"
            " to the group {group_name} as {role_name}"
        ),
    }


class UsersCancelledInvitationTemplate(BaseEmailTemplate):
    """User cancel invitation template"""

    name: str = _("User Cancelled Invitation")
    event_name: str = "users:cancelled:invitation"
    subject: str = _("{APP_NAME} - Invitation to {group_name} cancelled")
    files_path: dict[str:str] = {
        "html": "emails/users/invitation.html",
        "txt": "emails/users/invitation.txt",
    }

    context = {
        "email": "{email}",
        "logo": "{EMAIL_LOGO}",
        "title": _("Invitation to group {group_name} cancelled"),
        "content_title": _("Hi !"),
        "paragraph_1": _(
            "Invitation to group {group_name} was cancelled by {from_first_name}"
        ),
    }
