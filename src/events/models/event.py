from dataclasses import dataclass, field

from .base_model import BaseModel


@dataclass
class Event(BaseModel):
    tenant_id: str
    name: str
    data: dict = field(default_factory=dict)
