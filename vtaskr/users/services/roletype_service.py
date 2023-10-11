from sqlalchemy.orm import Session

# from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.models import RoleType
from vtaskr.users.persistence import RoleTypeDB
from vtaskr.users.services.permission_service import PermissionControl


class RoleTypeService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.roletype_db = RoleTypeDB()
        self.control = PermissionControl(self.session)

    def get_default_admin(self) -> RoleType:
        """Looking for a default roletype named: Admin"""

        admin_roletype = RoleType(name="Admin", group_id=None)
        roletype, created = self.roletype_db.get_or_create(
            session=self.session, roletype=admin_roletype
        )

        if created:
            from .right_service import RightService

            right_service = RightService(self.session)
            right_service.create_admin_rights(roletype=roletype)

        return roletype

    def get_default_observer(self) -> RoleType:
        """Looking for a default roletype named: Observer"""

        observer_roletype = RoleType(name="Observer", group_id=None)
        roletype, created = self.roletype_db.get_or_create(
            session=self.session, roletype=observer_roletype
        )

        if created:
            from .right_service import RightService

            right_service = RightService(self.session)
            right_service.create_observer_rights(roletype=roletype)

        return roletype

    def create_custom_roletype(self, name: str, group_id: str) -> RoleType:
        roletype = RoleType(name=name, group_id=group_id)
        roletype, _created = self.roletype_db.get_or_create(
            session=self.session, roletype=roletype
        )

        return roletype
