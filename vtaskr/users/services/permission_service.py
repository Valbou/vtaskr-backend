from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.persistence.sqlalchemy.adapters import GroupDB, UserDB


class PermissionControl:
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def can(
        self,
        permission: Permissions,
        user_id: str,
        group_id_resource: str,
        resource: Resources,
    ) -> bool:
        user_db = UserDB()

        return user_db.has_permissions(
            self.session, user_id, resource, permission, group_id_resource
        )

    def all_tenants_with_access(
        self, permission: Permissions, user_id: str, resource: Resources
    ) -> list[str]:
        group_db = GroupDB()

        return group_db.accessibles_by_user_with_permission(
            session=self.session,
            permission=permission,
            user_id=user_id,
            resource=resource,
        )
