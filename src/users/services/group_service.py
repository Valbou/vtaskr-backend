from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions
from src.users.models import Group, Role
from src.users.persistence import GroupDBPort, RoleDBPort
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
        self.role_db: RoleDBPort = self.services.persistence.get_repository(
            APP_NAME, "Role"
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
                        resource="Group",
                    )
                    else None
                )
        return None

    def update_group(self, user_id: str, group: Group) -> bool:
        """Update a group if update permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session, Permissions.UPDATE, user_id, group.id, resource="Group"
            ):
                self.group_db.save(session, group)
                session.commit()
                return True
            return False

    def delete_group(self, user_id: str, group: Group) -> bool:
        """Delete all roles before the group if delete permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session, Permissions.DELETE, user_id, group.id, resource="Group"
            ):
                self.group_db.delete(session, group)
                session.commit()
                return True
            return False

    def get_members(self, user_id: str, group_id: str) -> Role | None:
        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session, Permissions.READ, user_id, group_id, resource="Group"
            ):
                roles = self.role_db.get_group_roles(session, group_id=group_id)

                return roles
            return None
