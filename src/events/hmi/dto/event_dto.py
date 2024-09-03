from dataclasses import dataclass

from src.events.models import Event


@dataclass
class EventDTO:
    id: str
    tenant_id: str
    name: str
    data: dict
    created_at: str = ""


class EventDTOMapperDTO:
    @classmethod
    def model_to_dto(cls, event: Event) -> EventDTO:
        return EventDTO(
            id=event.id,
            created_at=event.created_at.isoformat() if event.created_at else "",
            name=event.name,
            tenant_id=event.tenant_id,
            data=event.data,
        )
