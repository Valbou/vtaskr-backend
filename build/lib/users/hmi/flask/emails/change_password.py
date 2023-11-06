from gettext import GNUTranslations
from typing import Tuple

from flask import render_template
from src.base.config import EMAIL_LOGO, LINK_TO_CHANGE_PASSWORD
from src.libs.notifications import AbstractBaseEmailContent


class ChangePasswordEmail(AbstractBaseEmailContent):
    logo = EMAIL_LOGO

    def __init__(
        self, trans: GNUTranslations, to: list[str], first_name: str, hash: str
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
        s1, s2, s3, _, s4 = self.get_trad(first_name)
        self.to_emails = to
        self.text = f"""
        \n{s1}\n{s2}\n{s3} {s4}\n{change_email_link}
        """

    def email_context(self, first_name: str, change_email_link: str) -> dict:
        title = self._("Change your Email").format(first_name=first_name)
        s1, s2, _, s3_bis, s4 = self.get_trad(first_name)
        content_title = s1
        content = f"""
        <p>
            {s2}
            <br />
            {s3_bis} {s4}.
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

    def get_trad(self, first_name: str) -> Tuple[str]:
        s1 = self._("Hi {first_name} !").format(first_name=first_name)
        s2 = self._("You request us to change your account password.")
        s3 = self._("Follow the link below to proceed")
        s3_bis = self._("Click on the following button to proceed")
        s4 = self._("(link available only 3 minutes)")
        return (s1, s2, s3, s3_bis, s4)
