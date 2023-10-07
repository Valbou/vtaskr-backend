from sqlalchemy.orm import Session

from vtaskr.users.models import RoleType
from vtaskr.users.persistence import RoleTypeDB


class RoleTypeService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.roletype_db = RoleTypeDB()

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

    def create_custom_roletype(self, name: str, group_id: str) -> RoleType:
        roletype = RoleType(name=name, group_id=group_id)
        roletype, _created = self.roletype_db.get_or_create(
            session=self.session, roletype=roletype
        )

        return roletype
