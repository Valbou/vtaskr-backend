from copy import copy
from typing import Callable

from src.ports import EventBusPort

from .config import EVENTS
from .event import Event, Observer


class EventBusService(EventBusPort):
    events: dict[str, list[Event]] = {}
    index: dict[str, list[Callable]] = {}

    def __init__(self) -> None:
        self.events = {}
        self.index = {}

        # Auto Subscribe for Observer classes
        observers = Observer.__subclasses__()
        for obs in observers:
            for event_type in EVENTS:
                observer = obs()
                if observer.auto_subscribe(event_type):
                    self.subscribe(event_type=event_type, function=observer)

    def set_context(self, **ctx) -> None:
        self.app = ctx.pop("app")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.execute()

    def emit(self, event_type: str, event: Event) -> None:
        if event_type not in self.events:
            self.events[event_type] = []

        self.events[event_type].append(event)

    def subscribe(self, event_type: str, function: Callable):
        if event_type not in self.index:
            self.index[event_type] = []

        self.index[event_type].append(function)

    def execute(self):
        local_events = copy(self.events)
        self.events.clear()

        for event_type, events in local_events.items():
            for event in events:
                observers = self.index.get(event_type, [])
                for obs in observers:
                    obs(self.app, event_type, event)

        if len(self.events):
            self.execute()
