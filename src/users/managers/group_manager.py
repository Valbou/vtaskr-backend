from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.users.models import Group, Role
from src.users.persistence import GroupDBPort, RoleDBPort
from src.users.settings import APP_NAME


class GroupManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.group_db: GroupDBPort = self.services.persistence.get_repository(
            APP_NAME, "Group"
        )
        self.role_db: RoleDBPort = self.services.persistence.get_repository(
            APP_NAME, "Role"
        )

    def get_group(self, session, user_id: str, group_id: str) -> Group | None:
        """Retrieve just a group if permission was given"""

        if self.services.identity.can(
            session,
            Permissions.READ,
            user_id,
            group_id,
            resource="Group",
        ):
            return self.group_db.load(session, group_id)

        return None

    def get_initial_group(self, session, user_id: str) -> Group | None:
        """Find initial group of a user, normally named Private"""

        return self.group_db.get_initial_user_group(session=session, user_id=user_id)

    def update_group(self, session, user_id: str, group: Group) -> bool:
        """Update a group if update permission was given"""

        if self.services.identity.can(
            session, Permissions.UPDATE, user_id, group.id, resource="Group"
        ):
            self.group_db.save(session, group)

            return True

        return False

    def delete_group(self, session, user_id: str, group: Group) -> bool:
        """Delete all roles before the group if delete permission was given"""

        if self.services.identity.can(
            session, Permissions.DELETE, user_id, group.id, resource="Group"
        ):
            self.group_db.delete(session, group)

            return True

        return False

    def get_members(self, session, user_id: str, group_id: str) -> list[Role]:
        if self.services.identity.can(
            session, Permissions.READ, user_id, group_id, resource="Group"
        ):
            roles = self.role_db.get_group_roles(session, group_id=group_id)

            return roles

        return []

    def get_all_groups(
        self,
        session,
        user_id: str,
        qs_filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        """Return all user associated groups"""

        return self.group_db.get_all_user_groups(
            session, user_id=user_id, filters=qs_filters
        )

    def create_group(self, session, group_name: str, is_private: bool = False) -> Group:
        """Create a new user group"""
        group = Group(name=group_name, is_private=is_private)
        self.group_db.save(session, group)

        return group
