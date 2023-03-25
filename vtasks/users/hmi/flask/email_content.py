from typing import List
from gettext import gettext as _

from flask import render_template

from vtasks.base.config import EMAIL_LOGO, LINK_TO_CHANGE_EMAIL, LINK_TO_CHANGE_PASSWORD
from vtasks.notifications import AbstractBaseEmailContent


class RegisterEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, to: List[str], first_name: str) -> None:
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name)
        )
        self.to_emails = to
        self.text = _(
            """
                Welcome {first_name} !
                Welcome in your new to do app. As of now, you can start to create tasks !
            """
        ).format(first_name=first_name)

    def email_context(self, first_name: str) -> dict:
        title = _("Registration Success {first_name}").format(first_name=first_name)
        content_title = _("Welcome {first_name} !").format(first_name=first_name)
        content = _(
            """
                <p>
                    Welcome in your new to do app. As of now, you can start to create tasks !
                </p>
            """
        )
        call_to_action = _("Enjoy !")

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": call_to_action,
        }
        return context


class LoginEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, to: List[str], first_name: str, code: str) -> None:
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, code)
        )
        self.to_emails = to
        self.text = _(
            """
Hi {first_name} !
To finish login process (2FA), please copy/paste the following code: {code}
This code stay valid only three minutes, after, you need to make a new login attempt.
            """
        ).format(first_name=first_name, code=code)

    def email_context(self, first_name: str, code: str) -> dict:
        title = _("New login with your account")
        content_title = _("Hi {first_name} !").format(first_name=first_name)
        content = _(
            """
                <p>
                    To finish login process (2FA), please copy/paste the following code:
                </p>
                <p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
                    {code}
                </p>
                <p>
                    This code stay valid only three minutes, after,
                    you need to make a new login attempt.
                </p>
            """
        ).format(code=code)

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": None,
        }
        return context


class ChangeEmailToOldEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, to: List[str], first_name: str, code: str) -> None:
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, code)
        )
        self.to_emails = to
        self.text = _(
            """
Hi {first_name} !
You request us to change your email account.
We have sent to you an email, in your new email account.
Click on the email sent to your new account and copy/paste the following code into the form:
{code}
This old email will be remove of your account after proceed.
            """
        ).format(first_name=first_name, code=code)

    def email_context(self, first_name: str, code: str) -> dict:
        title = _("Change your Email").format(first_name=first_name)
        content_title = _("Hi {first_name} !").format(first_name=first_name)
        content = _(
            """
                <p>
                    You request us to change your email account.
                    We have sent to you an email, in your new email account.<br />
                    Click on the email sent to your new account and copy/paste the
                    following code into the form:
                </p>
                <p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
                    {code}
                </p>
                <p>This old email will be removed of your account after proceed.</p>
            """
        ).format(code=code)

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": None,
        }
        return context


class ChangeEmailToNewEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, to: List[str], first_name: str, hash: str) -> None:
        change_email_link = (
            f"{LINK_TO_CHANGE_EMAIL}&hash={hash}&email={to}"
            if "?" in LINK_TO_CHANGE_EMAIL
            else f"{LINK_TO_CHANGE_EMAIL}?hash={hash}&email={to}"
        )

        self.html = render_template(
            "emails/simple_text.html",
            **self.email_context(first_name, change_email_link),
        )
        self.to_emails = to
        self.text = _(
            """
Hi {first_name} !
You request us to change your email account.
We sent you an email, in your old email account with a code required to complete the process.
Follow the link below to proceed:
{change_email_link}
            """
        ).format(first_name=first_name, change_email_link=change_email_link)

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = _("Change your Email").format(first_name=first_name)
        content_title = _("Hi {first_name} !").format(first_name=first_name)
        content = _(
            """
                <p>
                    You request us to change your email account.
                    We sent you an email, in your old email account with a code
                    required to complete the process.<br />
                    Click on the following button to proceed (link available only 3 minutes).
                </p>
                <p>This old email will be removed of your account after proceed.</p>
            """
        )

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": _("Change now"),
            "call_to_action_link": change_email_link,
        }
        return context


class ChangePasswordEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, to: List[str], first_name: str, hash: str) -> None:
        change_email_link = (
            f"{LINK_TO_CHANGE_PASSWORD}&hash={hash}&email={to}"
            if "?" in LINK_TO_CHANGE_PASSWORD
            else f"{LINK_TO_CHANGE_PASSWORD}?hash={hash}&email={to}"
        )

        self.html = render_template(
            "emails/simple_text.html",
            **self.email_context(first_name, change_email_link),
        )
        self.to_emails = to
        self.text = _(
            """
Hi {first_name} !
You request us to change your account password.
Follow the link below to proceed:
{change_email_link}
            """
        ).format(first_name=first_name, change_email_link=change_email_link)

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = _("Change your Email").format(first_name=first_name)
        content_title = _("Hi {first_name} !").format(first_name=first_name)
        content = _(
            """
                <p>
                    You request us to change your account password.
                    Follow the link below to proceed (link available only 3 minutes).
                </p>
            """
        )

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": _("Change now"),
            "call_to_action_link": change_email_link,
        }
        return context
