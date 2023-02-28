from typing import List
from gettext import GNUTranslations

from flask import render_template

from vtasks.base.config import EMAIL_LOGO, LINK_TO_CHANGE_EMAIL, LINK_TO_CHANGE_PASSWORD
from vtasks.notifications import AbstractBaseEmailContent


class RegisterEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, trans: GNUTranslations, to: List[str], first_name: str) -> None:
        self._ = trans.gettext
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name)
        )
        self.to_emails = to
        self.text = f"""
{self._("Welcome {first_name} !")}
{self._("Welcome in your new to do app. As of now, you can start to create tasks !")}
        """.format(
            first_name=first_name
        )

    def email_context(self, first_name: str) -> dict:
        title = self._("Registration Success {first_name}").format(
            first_name=first_name
        )
        content_title = self._("Welcome {first_name} !").format(first_name=first_name)
        content = f"""
<p>
    {self._("Welcome in your new to do app. As of now, you can start to create tasks !")}
</p>
        """
        call_to_action = self._("Enjoy !")

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

    def __init__(
        self, trans: GNUTranslations, to: List[str], first_name: str, code: str
    ) -> None:
        self._ = trans.gettext
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, code)
        )
        self.to_emails = to
        self.text = f"""
{self._("Hi {first_name} !")}
{self._("To finish login process (2FA), please copy/paste the following code: {code}")}
{self._(
    "This code stay valid only three minutes, after,"
    "you need to make a new login attempt."
)}
        """.format(
            first_name=first_name, code=code
        )

    def email_context(self, first_name: str, code: str) -> dict:
        title = self._("New login with your account")
        content_title = self._("Hi {first_name} !").format(first_name=first_name)
        content = f"""
<p>
    {self._("To finish login process (2FA), please copy/paste the following code:")}
</p>
<p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
    {"{code}"}
</p>
<p>
    {self._(
        "This code stay valid only three minutes, after,"
        "you need to make a new login attempt."
    )}
</p>
        """.format(
            code=code
        )

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

    def __init__(
        self, trans: GNUTranslations, to: List[str], first_name: str, code: str
    ) -> None:
        self._ = trans.gettext
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, code)
        )
        self.to_emails = to
        self.text = f"""
{self._("Hi {first_name} !")}
{self._("You request us to change your email account.")}
{self._("We have sent to you an email, in your new email account.")}
{self._(
    "Click on the email sent to your new account and"
    "copy/paste the following code into the form:"
)}
{"{code}"}
{self._("This old email will be remove of your account after proceed.")}
        """.format(
            first_name=first_name, code=code
        )

    def email_context(self, first_name: str, code: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        content_title = self._("Hi {first_name} !").format(first_name=first_name)
        content = f"""
<p>
    {self._("You request us to change your email account.")}
    {self._("We have sent to you an email, in your new email account.")}<br />
    {self._(
        "Click on the email sent to your new account and"
        "copy/paste the following code into the form:"
    )}
</p>
<p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
    {"{code}"}
</p>
<p>{self._("This old email will be remove of your account after proceed.")}</p>
            """.format(
            code=code
        )

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

    def __init__(
        self, trans: GNUTranslations, to: List[str], first_name: str, hash: str
    ) -> None:
        self._ = trans.gettext
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
        self.text = f"""
{self._("Hi {first_name} !")}
{self._("You request us to change your email account.")}
{self._(
    "We sent you an email, in your old email account"
    "with a code required to complete the process."
)}
{self._("Follow the link below to proceed")} {self._("(link available only 3 minutes)")}:
{self._("{change_email_link}")}
{self._("This old email will be removed of your account after proceed.")}
        """.format(
            first_name=first_name, change_email_link=change_email_link
        )

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        content_title = self._("Hi {first_name} !").format(first_name=first_name)
        content = f"""
<p>
    {self._("You request us to change your email account.")}
    {self._(
        "We sent you an email, in your old email account"
        "with a code required to complete the process."
    )}
    <br />
    {self._("Click on the following button to proceed")}
    {self._("(link available only 3 minutes)")}.
</p>
<p>{self._("This old email will be removed of your account after proceed.")}</p>
        """

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": self._("Change now"),
            "call_to_action_link": change_email_link,
        }
        return context


class ChangePasswordEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(
        self, trans: GNUTranslations, to: List[str], first_name: str, hash: str
    ) -> None:
        self._ = trans.gettext
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
        self.text = f"""
{self._("Hi {first_name} !")}
{self._("You request us to change your account password.")}
{self._("Follow the link below to proceed")}
{self._("{change_email_link}")}
        """.format(
            first_name=first_name, change_email_link=change_email_link
        )

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        content_title = self._("Hi {first_name} !").format(first_name=first_name)
        content = f"""
<p>
    {self._("You request us to change your account password.")}
    {self._("Click on the following button to proceed")}
    {self._("(link available only 3 minutes)")}.
</p>
        """

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": self._("Change now"),
            "call_to_action_link": change_email_link,
        }
        return context
