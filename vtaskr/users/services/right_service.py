from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.models import Right, RoleType
from vtaskr.users.persistence import RightDB
from vtaskr.users.services.permission_service import PermissionControl


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
        """Helper to add right to a roletype"""
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
