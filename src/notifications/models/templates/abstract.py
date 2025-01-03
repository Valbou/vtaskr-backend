from abc import ABC
from gettext import GNUTranslations

from flask import render_template
from src.notifications.exceptions import MissingTemplateFormatError
from src.notifications.settings import MessageType
from src.settings import APP_NAME


class AbstractTemplate(ABC):
    """Base for template creation"""

    event_type: MessageType
    event_name: str
    sender: str = APP_NAME
    name: str = "Abstract Template"
    files_path: dict[str:str] = {}
    subject: str = ""
    context: dict = {}

    def _get_subject(self, session: GNUTranslations) -> str:
        return session.gettext(self.subject)

    def _get_context(self, session: GNUTranslations, data: dict) -> dict:
        return {k: session.gettext(v).format(**data) for k, v in self.context.items()}

    def interpolate_subject(self, session: GNUTranslations, data: dict) -> str:
        return self._get_subject(session=session).format(**data)

    def interpolate_content(
        self, session: GNUTranslations, format: str, data: dict
    ) -> str:
        context_data = {**data, **self._get_context(session=session, data=data)}
        try:
            return render_template(
                self.files_path[format],
                **context_data,
            )
        except IndexError:
            raise MissingTemplateFormatError(
                f"No {format} format available for "
                f"{self.event_type.value} {self.event_name}"
            )
