from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.models import Group, User
from vtaskr.users.persistence import GroupDB
from vtaskr.users.services.permission_service import PermissionControl

# TODO:
# Since foreign key are not permitted between bounded context
# Remove a group may create many orphan resources
# 1 - add a periodic script to remove all orphans
# 2 - remove all orphans when user delete a group
# 3 - protect group deletion if a resouce may become an orphan


class GroupService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.group_db = GroupDB()
        self.control = PermissionControl(self.session)

    def create_group(self, user: User, group_name: str) -> Group:
        """Create a new user group"""

        group = Group(name=group_name)
        self.group_db.save(self.session, group)

        from .roletype_service import RoleTypeService

        roletype_service = RoleTypeService(self.session)
        roletype = roletype_service.get_default_admin()

        from .role_service import RoleService

        role_service = RoleService(self.session)
        role_service.add_role(
            user_id=user.id, group_id=group.id, roletype_id=roletype.id
        )

        return group

    def create_private_group(self, user: User) -> Group:
        """Create a default mandatory group to use this app"""

        return self.create_group(user=user, group_name="Private")

    def get_all_groups(self, user_id: str) -> list[Group] | None:
        """Return all user associated groups"""

        return self.group_db.get_all_user_groups(self.session, user_id=user_id)

    def get_group(self, user_id: str, group_id: str) -> Group | None:
        """Retrieve just a group if permission was given"""

        group = self.group_db.load(self.session, group_id)

        if group:
            return (
                group
                if self.control.can(
                    Permissions.READ, user_id, group.id, resource=Resources.GROUP
                )
                else None
            )
        return None

    def update_group(self, user_id: str, group: Group) -> None:
        """Update a group if update permission was given"""

        if self.control.can(
            Permissions.UPDATE, user_id, group.id, resource=Resources.GROUP
        ):
            self.group_db.save(self.session, group)

    def delete_group(self, user_id: str, group: Group) -> None:
        """Delete all roles before the group if delete permission was given"""

        if self.control.can(
            Permissions.DELETE, user_id, group.id, resource=Resources.GROUP
        ):
            self.group_db.delete(self.session, group)
