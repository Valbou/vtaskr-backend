from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.notifications.models import Template
from src.notifications.persistence.ports import TemplateDBPort
from src.notifications.persistence.sqlalchemy.querysets import TemplateQueryset
from src.ports import MessageType


class TemplateDB(TemplateDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = TemplateQueryset()

    def update(self, session: Session, template: Template) -> bool:
        self.qs.update().id(template.id).values(
            name=template.name,
            sender=template.sender,
            subject=template.subject,
            event_name=template.event_name,
            event_type=template.event_type,
            html=template.html,
            text=template.text,
            updated_at=datetime.now(tz=ZoneInfo("UTC")),
        )
        session.execute(self.qs.statement)

    def get_template_for_event(
        self, session: Session, event_name: str, event_type: MessageType
    ) -> Template | None:
        self.qs.event_template(event_name=event_name, event_type=event_type)
        return session.scalars(self.qs.statement).one_or_none()
