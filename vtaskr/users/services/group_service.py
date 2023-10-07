from sqlalchemy.orm import Session

from vtaskr.users.models import Group, User
from vtaskr.users.persistence import GroupDB


class GroupService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.group_db = GroupDB()

    def create_group(self, user: User, group_name: str):
        """Create a new user group"""

        group = Group(name=group_name)
        self.group_db.save(self.session, group)

        from .roletype_service import RoleTypeService

        roletype_service = RoleTypeService(self.session)
        roletype = roletype_service.get_default_admin()

        from .role_service import RoleService

        role_service = RoleService(self.session)
        role_service.add_role(
            user_id=user.id, group_id=group.id, roletype_id=roletype.id
        )

        return group

    def create_private_group(self, user: User) -> Group:
        """Create a default mandatory group to use this app"""

        return self.create_group(user=user, group_name="Private")
