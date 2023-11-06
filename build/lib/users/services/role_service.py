from sqlalchemy.orm import Session

from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.users.models import Role
from src.users.persistence import RoleDB
from src.users.services.permission_service import PermissionControl

# TODO:
# User cannot delete/change an admin rôle if he is the last admin
# Options are :
# 1 - He must delete group to process
# 2 - Choose an new admin and remove/change his role after
# Important to avoid orphan groups with locked users


class RoleService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.role_db = RoleDB()
        self.control = PermissionControl(self.session)

    def add_role(self, user_id: str, group_id: str, roletype_id: str) -> Role:
        """
        Add a role for internal usage in other services only
        (example: admin access to a new group or unittesting)

        For an external request, use create_role() instead, with permission controls
        """
        role = Role(
            user_id=user_id,
            group_id=group_id,
            roletype_id=roletype_id,
        )

        self.role_db.save(self.session, role)

        return role

    def create_role(self, user_id: str, role: Role) -> Role | None:
        """Add a role with permission controls"""

        if self.control.can(
            Permissions.CREATE,
            user_id=user_id,
            group_id_resource=role.group_id,
            resource=Resources.GROUP,
            exception=True,
        ):
            self.role_db.save(self.session, role)
            return role
        return None

    def get_role(self, user_id, role_id) -> Role | None:
        """Return the role expected if user has read permission"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.CREATE, user_id=user_id, resource=Resources.ROLE
        )
        return self.role_db.get_a_user_role(
            self.session, user_id, role_id, group_ids=group_ids
        )

    def get_all_roles(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Role]:
        """Return a list of all user's roles"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.CREATE, user_id=user_id, resource=Resources.ROLE
        )
        return self.role_db.get_all_user_roles(
            self.session, user_id, group_ids=group_ids, filters=qs_filters
        )

    def update_role(self, user_id: str, role: Role) -> bool:
        """Update a role if update permission was given"""

        # A user can't change his roles
        if role.user_id != user_id and self.control.can(
            Permissions.UPDATE, user_id, role.group_id, resource=Resources.ROLE
        ):
            self.role_db.save(self.session, role)
            return True
        return False

    def delete_role(self, user_id: str, role: Role) -> bool:
        """Delete a role if delete permission was given"""

        # A user can't change his roles
        if role.user_id != user_id and self.control.can(
            Permissions.DELETE, user_id, role.group_id, resource=Resources.ROLE
        ):
            self.role_db.delete(self.session, role)
            return True
        return False
