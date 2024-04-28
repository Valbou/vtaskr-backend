from dataclasses import dataclass

from src.logtrail.models import LogTrail


@dataclass
class LogTrailDTO:
    id: str
    log_type: str
    content: str
    created_at: str = ""


class LogTrailDTOMapperDTO:
    @classmethod
    def model_to_dto(
        cls,
        logtrail: LogTrail,
    ) -> LogTrailDTO:
        return LogTrailDTO(
            id=logtrail.id,
            created_at=logtrail.created_at.isoformat(),
            log_type=logtrail.log_type,
            content=logtrail.content,
        )
