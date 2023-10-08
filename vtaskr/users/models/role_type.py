from dataclasses import dataclass
from datetime import datetime

from pytz import utc

from vtaskr.libs.secutity.utils import get_id


@dataclass
class RoleType:
    id: str = ""
    name: str = ""
    group_id: str | None = None  # group specific RoleType or global if none
    created_at: datetime = datetime.now(utc)

    def __init__(
        self,
        name: str,
        group_id: str | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.name = name
        self.group_id = group_id
