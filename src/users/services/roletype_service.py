from sqlalchemy.orm import Session

from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.users.models import RoleType
from src.users.persistence import RoleTypeDB
from src.users.services.permission_service import PermissionControl


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

    def get_roletype(self, user_id: str, roletype_id: str) -> RoleType | None:
        """Return the roletype expected if user has read permission"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.READ, user_id=user_id, resource=Resources.ROLETYPE
        )

        return self.roletype_db.get_a_user_roletype(
            self.session, roletype_id, group_ids=group_ids
        )

    def get_all_roletypes(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[RoleType]:
        """Return a list of all user's available roletypes"""

        group_ids = self.control.all_tenants_with_access(
            Permissions.READ, user_id=user_id, resource=Resources.ROLETYPE
        )

        return self.roletype_db.get_all_user_roletypes(
            self.session, group_ids=group_ids, filters=qs_filters
        )

    def update_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Update a roletype if update permission was given"""

        # A user can't change global roletypes
        if self.control.can(
            Permissions.UPDATE, user_id, roletype.group_id, resource=Resources.ROLETYPE
        ):
            self.roletype_db.save(self.session, roletype)
            return True
        return False

    def delete_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Delete a roletype if delete permission was given"""

        # A user can't delete global roletypes
        if roletype.group_id and self.control.can(
            Permissions.DELETE, user_id, roletype.group_id, resource=Resources.ROLETYPE
        ):
            self.roletype_db.delete(self.session, roletype)
            return True
        return False
