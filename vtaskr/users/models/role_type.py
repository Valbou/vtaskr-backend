from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pytz import utc

from vtaskr.libs.secutity.utils import get_id


@dataclass
class RoleType:
    id: str = ""
    name: str = ""
    group_id: Optional[str] = None  # group specific RoleType or global if none
    created_at: datetime = datetime.now(utc)

    def __init__(
        self,
        name: str,
        group_id: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.name = name
        self.group_id = group_id
