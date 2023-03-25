class PermissionControl:
    """
    Control permissions to access a resource.
    Basic control check only ownership
    """

    def is_owner(self, user_id: str, resource_user_id: str) -> bool:
        return user_id == resource_user_id
