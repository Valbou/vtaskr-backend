from src.events.models import Event
from src.events.persistence import EventDBPort
from src.events.settings import APP_NAME
from src.libs.dependencies import DependencyInjector


class EventService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event_db: EventDBPort = self.services.persistence.get_repository(
            APP_NAME, "Event"
        )

    def get_all(self) -> list[Event]:
        with self.services.persistence.get_session() as session:
            return self.event_db.get_all(session=session)

    def get_all_from_tenant_id(self, tenant_id: str) -> list[Event]:
        with self.services.persistence.get_session() as session:
            return self.event_db.get_all_from_tenant(
                session=session, tenant_id=tenant_id
            )

    def add(
        self,
        tenant_id: str,
        event_name: str,
        data: dict,
    ) -> Event:
        event = Event(
            tenant_id=tenant_id,
            event_name=event_name,
            data=data,
        )

        with self.services.persistence.get_session() as session:
            self.event_db.save(session=session, obj=event)

        return event
