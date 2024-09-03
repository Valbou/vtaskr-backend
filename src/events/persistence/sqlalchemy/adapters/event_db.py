from sqlalchemy.orm import Session

from src.events.models import Event
from src.events.persistence.ports import EventDBPort
from src.events.persistence.sqlalchemy.querysets import EventQueryset
from src.libs.sqlalchemy.default_adapter import DefaultDB


class EventDB(EventDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = EventQueryset()

    def get_all_from_tenant(self, session: Session, tenant_id: str) -> list[Event]:
        self.qs.select().where(Event.tenant_id == tenant_id).order_by(
            created_at="DESC"
        ).limit(100)
        return session.scalars(self.qs.statement).all()
