from src.events.models import Event
from src.events.persistence import EventDBPort
from src.events.settings import APP_NAME
from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions


class EventManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event_db: EventDBPort = self.services.persistence.get_repository(
            APP_NAME, "Event"
        )

    def get_all_user_events(self, session, user_id: str, tenant_id: str) -> list[Event]:
        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Event",
        )

        if tenant_id in tenant_ids:
            return self.event_db.get_all_from_tenant(
                session=session, tenant_id=tenant_id
            )

        return []

    def add(self, session, tenant_id: str, event_name: str, data: dict) -> Event:
        event = Event(
            tenant_id=tenant_id,
            name=event_name,
            data=data,
        )

        self.event_db.save(session, obj=event)

        return event

    def bulk_add(self, session, events: list[Event]) -> list[Event]:
        return self.event_db.bulk_save(session, objs=events)
