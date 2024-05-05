from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class BaseModel:
    id: str = field(kw_only=True, default="")
    created_at: datetime | None = field(kw_only=True, default=None)

    def __post_init__(self):
        self._set_id()

    def _set_id(self):
        if not self.id:
            self.id = uuid4().hex


@dataclass
class BaseModelUpdate(BaseModel):
    updated_at: datetime | None = field(kw_only=True, default=None)

    def __post_init__(self):
        super().__post_init__()
