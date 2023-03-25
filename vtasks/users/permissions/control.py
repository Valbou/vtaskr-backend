from typing import Any

from vtasks.users import User


class PermissionControl:
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def is_owner(self, user: User, resource: Any) -> bool:
        return hasattr(resource, "user_id") and user.id == resource.user_id
