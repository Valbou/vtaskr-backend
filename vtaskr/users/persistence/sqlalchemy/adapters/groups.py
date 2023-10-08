from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.models import Group, Right, Role, RoleType
from vtaskr.users.persistence.ports import AbstractGroupPort
from vtaskr.users.persistence.sqlalchemy.querysets import GroupQueryset


class GroupDB(AbstractGroupPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = GroupQueryset()

    def update(self, session: Session, group: Group, autocommit: bool = True) -> bool:
        self.qs.update().id(group.id).values(name=group.name)
        session.execute(self.qs.statement)

        if autocommit:
            session.commit()

    def accessibles_by_user_with_permission(
        self,
        session: Session,
        permission: Permissions,
        user_id: str,
        resource: Resources,
    ) -> list[str] | None:
        self.qs.select(Group.id).join(Group.roles).join(Role.roletype).join(
            RoleType.rights
        ).where(
            Role.user_id == user_id,
            Right.resource == resource,
            Right.permissions.bitwise_and(permission) > 0,
        )

        return [r[0] for r in session.execute(self.qs.statement)]

    def get_all_user_groups(self, session: Session, user_id: str) -> list[Group] | None:
        self.qs.join(Group.roles).where(
            Role.user_id == user_id,
        )

        groups = list(session.execute(self.qs.statement))
        return groups
