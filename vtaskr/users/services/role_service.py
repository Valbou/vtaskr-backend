from sqlalchemy.orm import Session

# from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.models import Role
from vtaskr.users.persistence import RoleDB
from vtaskr.users.services.permission_service import PermissionControl

# TODO:
# User cannot delete/change an admin rôle if he is the last admin
# Options are :
# 1 - He must delete group to process
# 2 - Choose an new admin and remove/change his role after
# Important to avoid orphan groups with locked users


class RoleService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.role_db = RoleDB()
        self.control = PermissionControl(self.session)

    def add_role(self, user_id: str, group_id: str, roletype_id: str) -> Role:
        """Add a role"""
        role = Role(
            user_id=user_id,
            group_id=group_id,
            roletype_id=roletype_id,
        )

        self.role_db.save(self.session, role)

        return role
