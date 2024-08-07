from sqlalchemy.orm import Session

from src.libs.hmi.querystring import Filter
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Role
from src.users.persistence.ports import RoleDBPort
from src.users.persistence.sqlalchemy.querysets import RoleQueryset


class RoleDB(RoleDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RoleQueryset()

    def update(self, session: Session, role: Role) -> bool:
        self.qs.update().id(role.id).values(roletype_id=role.roletype_id)
        session.execute(self.qs.statement)

    def get_a_user_role(
        self, session: Session, user_id: str, role_id: str, group_ids: list[str]
    ) -> Role | None:
        self.qs.select().both_is_mine_and_is_under_my_control(
            user_id=user_id, group_ids=group_ids
        ).id(role_id)

        return session.scalars(self.qs.statement).one_or_none()

    def get_all_user_roles(
        self,
        session: Session,
        user_id: str,
        group_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[Role]:
        (
            self.qs.select()
            .from_filters(filters)
            .both_is_mine_and_is_under_my_control(user_id=user_id, group_ids=group_ids)
        )

        roles = session.scalars(self.qs.statement).all()
        return roles

    def get_group_roles(self, session: Session, group_id: str) -> list[Role]:
        self.qs.select().group_roles(group_id)

        roles = session.scalars(self.qs.statement).all()
        return roles
