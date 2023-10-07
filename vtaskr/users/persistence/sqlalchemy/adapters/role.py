from sqlalchemy.orm import Session

from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.models import Role
from vtaskr.users.persistence.ports import AbstractRolePort
from vtaskr.users.persistence.sqlalchemy.querysets import RoleQueryset


class RoleDB(AbstractRolePort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RoleQueryset()

    def update(self, session: Session, role: Role, autocommit: bool = True) -> bool:
        self.qs.update().id(role.id).values(roletype_id=role.roletype_id)
        session.execute(self.qs.statement)

        if autocommit:
            session.commit()
