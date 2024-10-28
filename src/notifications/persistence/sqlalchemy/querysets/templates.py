from typing import Self

from src.libs.sqlalchemy.queryset import Queryset
from src.notifications.models import Template
from src.ports import MessageType


class TemplateQueryset(Queryset):
    def __init__(self):
        super().__init__(Template)

    def event_template(self, event_name: str, event_type: MessageType) -> Self:
        self._query = self._query.where(
            self.qs_class.event_name == event_name,
            self.qs_class.event_type == event_type,
        )
        return self
