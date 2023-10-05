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

    def get_permissions(self, user_id: str, group_id: str) -> list[Permissions]:
        # TODO: Repository query needed !
        user_db = UserDB()
        user = user_db.with_group_permissions(self.session, user_id, group_id)

        for role in user.roles:
            for right in role.roletype.rights:
                pass

        permissions = []
        return permissions

    def has_permission(self, needed: Permissions, required: Permissions) -> bool:
        return
