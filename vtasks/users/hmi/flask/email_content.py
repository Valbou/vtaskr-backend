from typing import List
from gettext import gettext as _

from flask import render_template

from vtasks.base.config import BASE64_LOGO
from vtasks.notifications import AbstractBaseEmailContent


class RegisterEmail(AbstractBaseEmailContent):
    logo = BASE64_LOGO

    def __init__(self, to: List[str], first_name: str, last_name: str) -> None:
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, last_name)
        )
        self.to_emails = to
        self.text = f"""
Welcome {first_name} {last_name} !
Welcome in your new to do app. As of now, you can start to create tasks !
        """

    def email_context(self, first_name: str, last_name: str) -> dict:
        title = _("Registration Success {first_name}").format(first_name=first_name)
        content_title = _("Welcome {first_name} {last_name} !").format(
            first_name=first_name, last_name=last_name
        )
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
    logo = BASE64_LOGO

    def __init__(
        self, to: List[str], first_name: str, last_name: str, code: str
    ) -> None:
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name, last_name, code)
        )
        self.to_emails = to
        self.text = f"""
Hi {first_name} {last_name} !
To finish login process (2FA), please copy/paste the following code: {code}
This code stay valid only three minutes, after, you need to make a new login attempt.
        """

    def email_context(self, first_name: str, last_name: str, code: str) -> dict:
        title = _("New login with your account").format(first_name=first_name)
        content_title = _("Hi {first_name} {last_name} !").format(
            first_name=first_name, last_name=last_name
        )
        content = _(
            f"""
<p>
    To finish login process (2FA), please copy/paste the following code:
</p>
<p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
    {code}
</p>
<p>This code stay valid only three minutes, after, you need to make a new login attempt.</p>
            """
        )

        context = {
            "logo": self.logo,
            "title": title,
            "content_title": content_title,
            "content": content,
            "call_to_action": None,
        }
        return context
