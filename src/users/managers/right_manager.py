from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.users.models import Right, RoleType
from src.users.persistence import RightDBPort
from src.users.settings import APP_NAME


class RightManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.right_db: RightDBPort = self.services.persistence.get_repository(
            APP_NAME, "Right"
        )

    def create_observer_rights(self, session, roletype_id: str) -> int:
        """Give reader rights on all resources for the given roletype (Admin)"""

        num_rights = len(
            [
                self.right_db.save(
                    session,
                    Right(
                        roletype_id=roletype_id,
                        resource=res,
                        permissions=[
                            Permissions.READ,
                        ],
                    ),
                )
                for res in self.services.identity.get_resources()
            ]
        )

        return num_rights

    def clean_all_rights(self, session, roletype_id: str) -> None:
        """Remove all rights to a roletype"""

        self.right_db.delete_roletype_rights(session=session, roletype_id=roletype_id)

    def create_admin_rights(self, session, roletype_id: str) -> int:
        """Give all rights on all resources for the given roletype (Admin)"""

        num_rights = len(
            [
                self.right_db.save(
                    session,
                    Right(
                        roletype_id=roletype_id,
                        resource=res,
                        permissions=[perm for perm in Permissions],
                    ),
                )
                for res in self.services.identity.get_resources()
            ]
        )

        return num_rights

    def add_right(
        self,
        roletype_id: str,
        resource: str,
        permissions: list[Permissions] | Permissions,
    ) -> Right:
        """
        Helper to add right to a roletype
        Prefer create_right for unsafe use
        """

        if isinstance(permissions, Permissions):
            permissions = [
                permissions,
            ]

        right = Right(
            roletype_id=roletype_id,
            resource=resource,
            permissions=permissions,
        )

        with self.services.persistence.get_session() as session:
            self.right_db.save(session, right)
            session.commit()

        return right

    def create_right(self, user_id: str, group_id: str, right: Right) -> Right | None:
        """Add a right with permission controls"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.CREATE,
                user_id=user_id,
                group_id_resource=group_id,
                resource="RoleType",
                exception=True,
            ):
                self.right_db.save(session, right)
                session.commit()

                return right

        return None

    def get_right(self, user_id, right_id) -> Right | None:
        """Return the right expected if user has read permission"""

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.READ, user_id=user_id, resource="RoleType"
            )
            return self.right_db.get_a_user_right(
                session, user_id, right_id, group_ids=group_ids
            )

    def get_all_rights(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Right]:
        """Return a list of all user's available rights"""

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.READ, user_id=user_id, resource="RoleType"
            )
            return self.right_db.get_all_user_rights(
                session, group_ids=group_ids, filters=qs_filters
            )

    def update_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Update a right if update permission was given"""

        with self.services.persistence.get_session() as session:
            # A user can't change global rights or right not bounded to the user
            if (
                right.roletype_id == roletype.id
                and roletype.group_id
                and self.services.identity.can(
                    session,
                    Permissions.UPDATE,
                    user_id,
                    roletype.group_id,
                    resource="RoleType",
                )
            ):
                self.right_db.save(session, right)
                session.commit()

                return True

        return False

    def delete_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Delete a right if delete permission was given"""

        with self.services.persistence.get_session() as session:
            # A user can't delete global rights or right not bounded to the user
            if (
                right.roletype_id == roletype.id
                and roletype.group_id
                and self.services.identity.can(
                    session,
                    Permissions.DELETE,
                    user_id,
                    roletype.group_id,
                    resource="RoleType",
                )
            ):
                self.right_db.delete(session, right)
                session.commit()

                return True

        return False
