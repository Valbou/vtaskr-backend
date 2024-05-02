from src.libs.dependencies import DependencyInjector
from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.users.models import Group
from src.users.persistence import GroupDBPort
from src.users.settings import APP_NAME

# TODO:
# Since foreign key are not permitted between bounded context
# Remove a group may create many orphan resources
# 1 - add a periodic script to remove all orphans
# 2 - remove all orphans when user delete a group
# 3 - protect group deletion if a resouce may become an orphan
# 4 - send an event to delete all resources with tenant id


class GroupService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.group_db: GroupDBPort = self.services.persistence.get_repository(
            APP_NAME, "Group"
        )

    def create_group(self, user_id: str, group_name: str) -> Group:
        """Create a new user group"""

        with self.services.persistence.get_session() as session:
            group = Group(name=group_name)
            self.group_db.save(session, group)

        from .roletype_service import RoleTypeService

        roletype_service = RoleTypeService(self.services)
        roletype = roletype_service.get_default_admin()

        from .role_service import RoleService

        role_service = RoleService(self.services)
        role_service.add_role(
            user_id=user_id, group_id=group.id, roletype_id=roletype.id
        )

        return group

    def create_private_group(self, user_id: str) -> Group:
        """Create a default mandatory group to use this app"""

        return self.create_group(user_id=user_id, group_name="Private")

    def get_all_groups(
        self,
        user_id: str,
        qs_filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        """Return all user associated groups"""

        with self.services.persistence.get_session() as session:
            return self.group_db.get_all_user_groups(
                session, user_id=user_id, filters=qs_filters
            )

    def get_group(self, user_id: str, group_id: str) -> Group | None:
        """Retrieve just a group if permission was given"""

        with self.services.persistence.get_session() as session:
            group = self.group_db.load(session, group_id)

            if group:
                return (
                    group
                    if self.services.identity.can(
                        session,
                        Permissions.READ,
                        user_id,
                        group.id,
                        resource=Resources.GROUP,
                    )
                    else None
                )
        return None

    def update_group(self, user_id: str, group: Group) -> bool:
        """Update a group if update permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session, Permissions.UPDATE, user_id, group.id, resource=Resources.GROUP
            ):
                self.group_db.save(session, group)
                return True
            return False

    def delete_group(self, user_id: str, group: Group) -> bool:
        """Delete all roles before the group if delete permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session, Permissions.DELETE, user_id, group.id, resource=Resources.GROUP
            ):
                self.group_db.delete(session, group)
                return True
            return False
