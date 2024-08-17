from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.users.models import RoleType
from src.users.persistence import RoleTypeDBPort
from src.users.settings import APP_NAME


class RoleTypeManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.roletype_db: RoleTypeDBPort = self.services.persistence.get_repository(
            APP_NAME, "RoleType"
        )

    def get_default_observer(self, session) -> tuple[RoleType, bool]:
        """Looking for a default roletype named: Observer"""

        observer_roletype = RoleType(name="Observer", group_id=None)
        roletype, created = self.roletype_db.get_or_create(
            session=session, roletype=observer_roletype
        )

        return roletype, created

    def get_default_admin(self, session) -> tuple[RoleType, bool]:
        """Looking for a default roletype named: Admin"""

        admin_roletype = RoleType(name="Admin", group_id=None)

        roletype, created = self.roletype_db.get_or_create(
            session=session, roletype=admin_roletype
        )

        return roletype, created

    def create_custom_roletype(self, name: str, group_id: str) -> tuple[RoleType, bool]:
        roletype = RoleType(name=name, group_id=group_id)

        with self.services.persistence.get_session() as session:
            roletype, created = self.roletype_db.get_or_create(
                session=session, roletype=roletype
            )

        return roletype, created

    def get_roletype(self, user_id: str, roletype_id: str) -> RoleType | None:
        """Return the roletype expected if user has read permission"""

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.READ, user_id=user_id, resource="RoleType"
            )

            roletype = self.roletype_db.get_a_user_roletype(
                session, roletype_id, group_ids=group_ids
            )

        return roletype

    def get_all_roletypes(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[RoleType]:
        """Return a list of all user's available roletypes"""

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.READ, user_id=user_id, resource="RoleType"
            )

            roletypes = self.roletype_db.get_all_user_roletypes(
                session, group_ids=group_ids, filters=qs_filters
            )

        return roletypes

    def update_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Update a roletype if update permission was given"""

        with self.services.persistence.get_session() as session:
            # A user can't change global roletypes
            if self.services.identity.can(
                session,
                Permissions.UPDATE,
                user_id,
                roletype.group_id,
                resource="RoleType",
            ):
                self.roletype_db.save(session, roletype)
                session.commit()

                return True

        return False

    def delete_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Delete a roletype if delete permission was given"""

        with self.services.persistence.get_session() as session:
            # A user can't delete global roletypes
            if roletype.group_id and self.services.identity.can(
                session,
                Permissions.DELETE,
                user_id,
                roletype.group_id,
                resource="RoleType",
            ):
                self.roletype_db.delete(session, roletype)
                session.commit()

                return True

        return False
