from typing import TypeVar

from src.libs.sqlalchemy.queryset import Queryset
from src.events.models import Event

TEventQueryset = TypeVar("TEventQueryset", bound="EventQueryset")


class EventQueryset(Queryset):
    def __init__(self):
        super().__init__(Event)

    def of_type(self, event_name: str) -> TEventQueryset:
        self._query = self._query.where(Event.name == event_name)
        return self
