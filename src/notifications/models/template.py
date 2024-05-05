from dataclasses import dataclass
from typing import TypeVar

from flask import render_template
from src.libs.sqlalchemy.base_model import BaseModelUpdate
from src.ports import MessageType

TTemplate = TypeVar("TTemplate", bound="Template")


@dataclass
class Template(BaseModelUpdate):
    """To store dynamically some data relative to templates"""

    event_type: MessageType
    event_name: str
    sender: str
    name: str = ""
    subject: str = ""
    html: str = ""
    text: str = ""

    def interpolate_subject(self, context: dict) -> str:
        return self.subject.format(**context)

    def interpolate_html(self, context: dict) -> str:
        return render_template(self.html, **context)

    def interpolate_text(self, context: dict) -> str:
        return render_template(self.text, **context)

    @classmethod
    def temp_template_from_context(cls, context: dict) -> TTemplate:
        template_name = context.pop("template")
        return Template(
            event_type=context.get("message_type"),
            event_name="None",
            sender=context.pop("sender"),
            name=template_name,
            subject=context.pop("subject"),
            html=template_name + ".html",
            text=template_name + ".txt",
        )
