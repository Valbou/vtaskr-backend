from dataclasses import dataclass, field

from .base_model import BaseModel


@dataclass
class LogTrail(BaseModel):
    tenant_id: str
    event_name: str
    event: dict = field(default_factory=dict)
