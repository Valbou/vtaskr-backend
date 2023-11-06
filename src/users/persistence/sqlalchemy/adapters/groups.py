from sqlalchemy.orm import Session

from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Group, Right, Role, RoleType
from src.users.persistence.ports import AbstractGroupPort
from src.users.persistence.sqlalchemy.querysets import GroupQueryset


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

    def get_all_user_groups(
        self,
        session: Session,
        user_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.select().join(Group.roles).where(
            Role.user_id == user_id,
        )

        groups = session.scalars(self.qs.statement).all()
        return groups
