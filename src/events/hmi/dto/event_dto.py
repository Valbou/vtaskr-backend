from dataclasses import dataclass

from src.events.models import Event


@dataclass
class EventDTO:
    id: str
    log_type: str
    content: str
    created_at: str = ""


class EventDTOMapperDTO:
    @classmethod
    def model_to_dto(
        cls,
        event: Event,
    ) -> EventDTO:
        return EventDTO(
            id=event.id,
            created_at=event.created_at.isoformat(),
            log_type=event.log_type,
            content=event.content,
        )
