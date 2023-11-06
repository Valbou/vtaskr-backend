from sqlalchemy.orm import Session

from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.users.models import Right, RoleType
from src.users.persistence import RightDB
from src.users.services.permission_service import PermissionControl


class RightService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.right_db = RightDB()
        self.control = PermissionControl(self.session)

    def create_admin_rights(self, roletype: RoleType) -> int:
        """Give all rights on all resources for the given roletype (Admin)"""
        num_rights = len(
            [
                self.right_db.save(
                    self.session,
                    Right(
                        roletype_id=roletype.id,
                        resource=res,
                        permissions=[perm for perm in Permissions],
                    ),
                    autocommit=False,
                )
                for res in Resources
            ]
        )

        # bulk insert
        self.session.commit()

        return num_rights

    def create_observer_rights(self, roletype: RoleType) -> int:
        """Give reader rights on all resources for the given roletype (Admin)"""
        num_rights = len(
            [
                self.right_db.save(
                    self.session,
                    Right(
                        roletype_id=roletype.id,
                        resource=res,
                        permissions=[
                            Permissions.READ,
                        ],
                    ),
                    autocommit=False,
                )
                for res in Resources
            ]
        )

        # bulk insert
        self.session.commit()

        return num_rights

    def add_right(
        self,
        roletype_id: str,
        resource: Resources,
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
        self.right_db.save(self.session, right)

        return right

    def create_right(self, user_id: str, group_id: str, right: Right) -> Right | None:
        """Add a right with permission controls"""

        if self.control.can(
            Permissions.CREATE,
            user_id=user_id,
            group_id_resource=group_id,
            resource=Resources.ROLETYPE,
            exception=True,
        ):
            self.right_db.save(self.session, right)
            return right
        return None

    def get_right(self, user_id, right_id) -> Right | None:
        """Return the right expected if user has read permission"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.READ, user_id=user_id, resource=Resources.ROLETYPE
        )
        return self.right_db.get_a_user_right(
            self.session, user_id, right_id, group_ids=group_ids
        )

    def get_all_rights(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Right]:
        """Return a list of all user's available rights"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.READ, user_id=user_id, resource=Resources.ROLETYPE
        )
        return self.right_db.get_all_user_rights(
            self.session, group_ids=group_ids, filters=qs_filters
        )

    def update_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Update a right if update permission was given"""

        # A user can't change global rights or right not bounded to the user
        if (
            right.roletype_id == roletype.id
            and roletype.group_id
            and self.control.can(
                Permissions.UPDATE,
                user_id,
                roletype.group_id,
                resource=Resources.ROLETYPE,
            )
        ):
            self.right_db.save(self.session, right)
            return True
        return False

    def delete_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Delete a right if delete permission was given"""

        # A user can't delete global rights or right not bounded to the user
        if (
            right.roletype_id == roletype.id
            and roletype.group_id
            and self.control.can(
                Permissions.DELETE,
                user_id,
                roletype.group_id,
                resource=Resources.ROLETYPE,
            )
        ):
            self.right_db.delete(self.session, right)
            return True
        return False
