from typing import ContextManager

from src.libs.iam.constants import Permissions, Resources
from src.ports import IdentityAccessManagementPort
from src.users.persistence.sqlalchemy.adapters import GroupDB, UserDB


class PermissionError(Exception):
    pass


class PermissionControl(IdentityAccessManagementPort):
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def can(
        self,
        session: ContextManager,
        permission: Permissions,
        user_id: str,
        group_id_resource: str,
        resource: Resources,
        exception: bool = True,
    ) -> bool:
        user_db = UserDB()

        permitted = user_db.has_permissions(
            session, user_id, resource, permission, group_id_resource
        )

        if not permitted and exception:
            raise PermissionError(
                f"User {user_id} has no permission {permission.name}"
                f" on {resource} in group {group_id_resource}"
            )

        return permitted

    def all_tenants_with_access(
        self,
        session: ContextManager,
        permission: Permissions,
        user_id: str,
        resource: Resources,
    ) -> list[str]:
        group_db = GroupDB()

        return group_db.accessibles_by_user_with_permission(
            session=session,
            permission=permission,
            user_id=user_id,
            resource=resource,
        )
