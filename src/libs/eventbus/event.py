from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


@dataclass
class Event:
    tenant_id: str
    event_type: str
    data: dict
    created_at: str | None = None

    def __post_init__(self):
        self.created_at = (
            self.created_at or datetime.now(tz=ZoneInfo("UTC")).isoformat()
        )


class Observer:
    def __call__(self, ctx: Any, event_type: str, event: Event) -> Any:
        event_type_undescored = self._clean_event_type(event_type)
        callable = getattr(self, event_type_undescored)
        if not callable:
            raise ValueError(f"Observer has no {event_type_undescored} method")
        callable(ctx, event_type, event)

    def auto_subscribe(self, event_type: list[str]) -> bool:
        event_type_undescored = self._clean_event_type(event_type)
        if hasattr(self, event_type_undescored):
            return True
        return False

    def _clean_event_type(self, event_type: str) -> str:
        return event_type.replace(":", "_")
