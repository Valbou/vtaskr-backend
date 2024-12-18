from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.users.models import Role
from src.users.persistence import RoleDBPort
from src.users.settings import APP_NAME

# TODO:
# User cannot delete/change an admin rôle if he is the last admin
# Options are :
# 1 - He must delete group to process
# 2 - Choose an new admin and remove/change his role after
# 3 - Remaining users with higher permissions become all admin,
#     if no users remain, delete the group
# Important to avoid orphan groups with locked users


class RoleManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.role_db: RoleDBPort = self.services.persistence.get_repository(
            APP_NAME, "Role"
        )

    def create_role(self, session, user_id: str, role: Role) -> Role | None:
        """Add a role with permission controls"""

        if self.services.identity.can(
            session,
            Permissions.CREATE,
            user_id=user_id,
            group_id_resource=role.group_id,
            resource="Group",
            exception=True,
        ):
            self.role_db.save(session, role)

            return role

        return None

    def add_role(self, session, user_id: str, group_id: str, roletype_id: str) -> Role:
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

        self.role_db.save(session, role)

        return role

    def get_role(self, session, user_id, role_id) -> Role | None:
        """Return the role expected if user has read permission"""

        group_ids = self.services.identity.all_tenants_with_access(
            session, Permissions.CREATE, user_id=user_id, resource="Role"
        )

        role = self.role_db.get_a_user_role(
            session, user_id, role_id, group_ids=group_ids
        )

        return role

    def get_all_roles(
        self, session, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Role]:
        """Return a list of all user's roles"""

        group_ids = self.services.identity.all_tenants_with_access(
            session, Permissions.READ, user_id=user_id, resource="Role"
        )
        roles = self.role_db.get_all_user_roles(
            session, user_id, group_ids=group_ids, filters=qs_filters
        )

        return roles

    def get_members(self, session, user_id: str, group_id: str) -> list[Role]:
        if self.services.identity.can(
            session, Permissions.READ, user_id, group_id, resource="Role"
        ):
            roles = self.role_db.get_group_roles(session, group_id=group_id)

            return roles

        return []

    def update_role(self, session, user_id: str, role: Role) -> bool:
        """Update a role if update permission was given"""

        # A user can't change his roles
        if role.user_id != user_id and self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            role.group_id,
            resource="Role",
        ):
            self.role_db.save(session, role)

            return True

        return False

    def delete_role(self, session, user_id: str, role: Role) -> bool:
        """Delete a role if delete permission was given"""

        # A user can't change his roles
        if role.user_id != user_id and self.services.identity.can(
            session,
            Permissions.DELETE,
            user_id,
            role.group_id,
            resource="Role",
        ):
            self.role_db.delete(session, role)

            return True

        return False
