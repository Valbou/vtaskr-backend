from typing import ContextManager

from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions
from src.ports import IdentityAccessManagementPort
from src.users.persistence import GroupDBPort, UserDBPort
from src.users.settings import APP_NAME


class PermissionError(Exception):
    pass


class PermissionControl(IdentityAccessManagementPort):
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def set_context(self, **ctx) -> None:
        self.app = ctx.pop("app")
        self.resources = ctx.pop("permissions_resources")
        self.services: DependencyInjector = self.app.dependencies

    def get_resources(self) -> list[str]:
        return self.resources

    def can(
        self,
        session: ContextManager,
        permission: Permissions,
        user_id: str,
        group_id_resource: str,
        resource: str,
        exception: bool = True,
    ) -> bool:
        user_db: UserDBPort = self.services.persistence.get_repository(APP_NAME, "User")

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
        resource: str,
    ) -> list[str]:
        group_db: GroupDBPort = self.services.persistence.get_repository(
            APP_NAME, "Group"
        )

        return group_db.accessibles_by_user_with_permission(
            session=session,
            permission=permission,
            user_id=user_id,
            resource=resource,
        )
