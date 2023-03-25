from gettext import GNUTranslations
from typing import List, Tuple

from flask import render_template
from vtasks.base.config import EMAIL_LOGO
from vtasks.notifications import AbstractBaseEmailContent


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
        s1, s2, s3, s4 = self.get_trad(first_name)
        self.text = f"""
        \n{s1}\n{s2}\n{s3} {code}\n{s4}
        """

    def email_context(self, first_name: str, code: str) -> dict:
        title = self._("New login with your account")
        s1, s2, s3, s4 = self.get_trad(first_name)
        content_title = s1
        content = f"""
        <p>
            {s2}<br />{s3}
        </p>
        <p style="font-size: 16px: font-weight: bolder; letter-spacing: 5px;">
            {code}
        </p>
        <p>
            {s4}
        </p>
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
        s2 = self._(
            "A login attempt was registered, "
            "if it's not you, please change your password."
        )
        s3 = self._("To login, please copy/paste the following code:")
        s4 = self._(
            "This code stay valid only three minutes, after,"
            "you need to make a new login attempt."
        )
        return (s1, s2, s3, s4)
