from gettext import GNUTranslations
from typing import Tuple

from flask import render_template

from src.base.config import EMAIL_LOGO
from src.libs.notifications import AbstractBaseEmailContent


class RegisterEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(self, trans: GNUTranslations, to: list[str], first_name: str) -> None:
        self._ = trans.gettext
        self.html = render_template(
            "emails/simple_text.html", **self.email_context(first_name)
        )
        self.to_emails = to
        s1, s2, s3 = self.get_trad(first_name)
        self.text = f"""
        \n{s1}\n{s2}\n{s3}
        """

    def email_context(self, first_name: str) -> dict:
        title = self._("Registration Success {first_name}").format(
            first_name=first_name
        )
        s1, s2, s3 = self.get_trad(first_name)
        content_title = s1
        content = f"""
        <p>
            {s2}<br />{s3}
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

    def get_trad(self, first_name: str) -> Tuple[str]:
        s1 = self._("Welcome {first_name} !").format(first_name=first_name)
        s2 = self._("Welcome in your new to do app management.")
        s3 = self._("As of now, you can login and start to create your tasks !")
        return (s1, s2, s3)
