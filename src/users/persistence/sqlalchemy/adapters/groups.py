from sqlalchemy.orm import Session

from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Group, Right, Role, RoleType
from src.users.persistence.ports import GroupDBPort
from src.users.persistence.sqlalchemy.querysets import GroupQueryset


class GroupDB(GroupDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = GroupQueryset()

    def update(self, session: Session, group: Group) -> bool:
        self.qs.update().id(group.id).values(
            name=group.name, description=group.description
        )
        session.execute(self.qs.statement)

    def accessibles_by_user_with_permission(
        self,
        session: Session,
        permission: Permissions,
        user_id: str,
        resource: str,
    ) -> list[str] | None:
        self.qs.select(Group.id).join(Group.roles).join(Role.roletype).join(
            RoleType.rights
        ).where(
            Role.user_id == user_id,
            Right.resource == resource,
            Right.permissions.bitwise_and(permission) > 0,
        )

        return [r[0] for r in session.execute(self.qs.statement)]

    def get_initial_user_group(
        self,
        session: Session,
        user_id: str,
    ) -> Group | None:
        self.qs.select().join(Group.roles).join(Role.roletype).where(
            Role.user_id == user_id,
            RoleType.name == "Admin",
            Group.is_private == True,  # noqa: E712
        ).order_by(created_at="ASC").limit(1)

        group = session.scalars(self.qs.statement).one_or_none()
        return group

    def get_all_user_groups(
        self,
        session: Session,
        user_id: str,
        filters: list[Filter] | None = None,
    ) -> list[Group] | None:
        self.qs.select().from_filters(filters).join(Group.roles).where(
            Role.user_id == user_id,
        )

        groups = session.scalars(self.qs.statement).all()
        return groups
