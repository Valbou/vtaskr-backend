from dataclasses import dataclass, field
from datetime import datetime

from pytz import utc

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.libs.secutity.utils import get_id


@dataclass
class Right:
    """EAV like model"""

    roletype_id: str
    resource: Resources = Resources.TASK
    id: str = ""
    created_at: datetime = datetime.now(utc)
    permissions: list[Permissions] = field(default_factory=list)

    def __init__(
        self,
        roletype_id: str,
        resource: Resources,
        permissions: list[Permissions] | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id or get_id()
        self.created_at = created_at or datetime.now(utc)
        self.roletype_id = roletype_id
        self.resource = resource
        self.permissions = permissions or [
            Permissions.READ,
        ]
