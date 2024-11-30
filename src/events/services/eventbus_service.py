from copy import copy
from typing import Callable

from src.events.models import Event
from src.ports import EventBusPort, ObserverPort

from .events_service import EventsService


class EventBusService(EventBusPort):
    events: dict[str, list[Event]] = {}
    index: dict[str, list[Callable]] = {}

    def __init__(self, **kwargs) -> None:
        self.events = {}
        self.index = {}

    def set_context(self, **ctx) -> None:
        self.app = ctx.pop("app")

        # Auto Subscribe for Observer classes
        observers = ObserverPort.__subclasses__()
        for obs in observers:
            self.subscribe(*obs.self_subscribe())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.execute()

    def emit(self, tenant_id: str, event_name: str, event_data: dict) -> None:
        if event_name not in self.events:
            self.events[event_name] = []

        self.events[event_name].append(
            Event(
                tenant_id=tenant_id,
                name=event_name,
                data=event_data,
            )
        )

    def subscribe(self, event_name: str, function: Callable):
        if event_name not in self.index:
            self.index[event_name] = []

        self.index[event_name].append(function)

    def execute(self):
        self.event_service = EventsService(services=self.app.dependencies)

        local_events = copy(self.events)
        self.events.clear()

        for event_name, events in local_events.items():
            self.event_service.bulk_add_events(events)

            for event in events:
                observers = self.index.get(event_name, [])
                for func in observers:
                    func(self.app, event_name, event.data)

        if len(self.events):
            self.execute()


class TestEventBusService(EventBusService):
    def execute(self):
        self.events.clear()
