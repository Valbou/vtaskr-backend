from sqlalchemy.orm import Session

from vtaskr.users.models import Role
from vtaskr.users.persistence import RoleDB


class RoleService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.role_db = RoleDB()

    def add_role(self, user_id: str, group_id: str, roletype_id: str) -> Role:
        """Add a role"""
        role = Role(
            user_id=user_id,
            group_id=group_id,
            roletype_id=roletype_id,
        )

        self.role_db.save(self.session, role)

        return role
