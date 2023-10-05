from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pytz import utc

from vtaskr.colors.models.color import Color
from vtaskr.libs.secutity.utils import get_id


@dataclass
class Role:
    id: str = ""
    user_id: str = ""
    group_id: str = ""
    roletype_id: str = ""
    color: Optional[Color] = None
    created_at: datetime = datetime.now(utc)

    def __init__(
        self,
        user_id: str,
        group_id: str,
        roletype_id: str,
        color: Optional[Color] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.color = color
        self.user_id = user_id
        self.group_id = group_id
        self.roletype_id = roletype_id
