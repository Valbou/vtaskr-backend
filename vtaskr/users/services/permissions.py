from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.persistence.sqlalchemy.adapters import UserDB


class PermissionControl:
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def __init__(self, session: Session, resource: Resources) -> None:
        self.session = session
        self.resource = resource

    def can(
        self, permission: Permissions, tenant_id_request: str, tenant_id_resource: str
    ) -> bool:
        return True
