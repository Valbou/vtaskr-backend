from gettext import GNUTranslations
from typing import Tuple

from flask import render_template
from src.base.config import EMAIL_LOGO, LINK_TO_CHANGE_EMAIL
from src.libs.notifications import AbstractBaseEmailContent


class ChangeEmailToOldEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(
        self, trans: GNUTranslations, to_emails: list[str], first_name: str, code: str
    ) -> None:
        self._ = trans.gettext
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, code)
        )
        self.to_emails = to_emails
        s1, s2, s3, s4, s5 = self.get_trad(first_name)
        self.text = f"""
        \n{s1}\n{s2}\n{s3}\n{s4} {code}\n{s5}
        """

    def email_context(self, first_name: str, code: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        s1, s2, s3, s4, s5 = self.get_trad(first_name)
        content_title = s1
        content = f"""
        <p>
            {s2}<br />{s3}<br />{s4}
        </p>
        <p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
            {code}
        </p>
        <p>{s5}</p>
            """

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": None,
        }
        return context

    def get_trad(self, first_name: str) -> Tuple[str]:
        s1 = self._("Hi {first_name} !").format(first_name=first_name)
        s2 = self._("You request to change your email account.")
        s3 = self._("We have sent to you an email, in your new email account.")
        s4 = self._(
            "Click on the email sent to your new account and"
            "copy/paste the following code into the form:"
        )
        s5 = self._("This old email will be remove of your account after proceed.")
        return (s1, s2, s3, s4, s5)


class ChangeEmailToNewEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(
        self, trans: GNUTranslations, to_emails: list[str], first_name: str, hash: str
    ) -> None:
        self._ = trans.gettext
        change_email_link = (
            f"{LINK_TO_CHANGE_EMAIL}&hash={hash}&email={to_emails}"
            if "?" in LINK_TO_CHANGE_EMAIL
            else f"{LINK_TO_CHANGE_EMAIL}?hash={hash}&email={to_emails}"
        )

        self.html = render_template(
            "emails/simple_text.html",
            **self.email_context(first_name, change_email_link),
        )
        self.to_emails = to_emails
        s1, s2, s3, _, s4_bis, s5, s6 = self.get_trad(first_name)
        self.text = f"""
        \n{s1}\n{s2}\n{s3}{s4_bis} {s5}:\n{change_email_link}\n{s6}
{self._("This old email will be removed of your account after proceed.")}
        """

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        s1, s2, s3, s4, _, s5, s6 = self.get_trad(first_name)
        content_title = s1
        content = f"""
        <p>
            {s2} {s3}
            <br />
            {s4} {s5}.
        </p>
        <p>{s6}</p>
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

    def get_trad(self, first_name: str) -> Tuple[str]:
        s1 = self._("Hi {first_name} !").format(first_name=first_name)
        s2 = self._("You request to change your email account.")
        s3 = self._(
            "We sent you an email, to your old email account "
            "with a code required to complete the process."
        )
        s4 = self._("Click on the following button to proceed")
        s4_bis = self._("Click on the following link to proceed")
        s5 = self._("(link available only 3 minutes)")
        s6 = self._("This old email will be removed of your account after proceed.")
        return (s1, s2, s3, s4, s4_bis, s5, s6)
