from src.events.managers import EventManager
from src.events.models import Event
from src.libs.dependencies import DependencyInjector


class EventsService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services

        self._define_managers()

    def _define_managers(self):
        """Define managers from domain (no DI here)"""

        self.event_manager = EventManager(services=self.services)

    def get_all_user_events(self, user_id: str, tenant_id: str) -> list[Event]:
        with self.services.persistence.get_session() as session:
            return self.event_manager.get_all_user_events(
                session=session, user_id=user_id, tenant_id=tenant_id
            )

    def add_event(self, tenant_id: str, event_name: str, data: dict) -> Event:
        with self.services.persistence.get_session() as session:
            return self.event_manager.add(
                session=session, tenant_id=tenant_id, event_name=event_name, data=data
            )

    def bulk_add_events(self, events: list[Event]) -> list[Event]:
        with self.services.persistence.get_session() as session:
            return self.event_manager.bulk_add(session, events=events)
