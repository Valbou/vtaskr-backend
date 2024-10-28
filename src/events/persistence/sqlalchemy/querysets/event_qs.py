from typing import Self

from src.events.models import Event
from src.libs.sqlalchemy.queryset import Queryset


class EventQueryset(Queryset):
    def __init__(self):
        super().__init__(Event)

    def of_type(self, event_name: str) -> Self:
        self._query = self._query.where(Event.name == event_name)
        return self
