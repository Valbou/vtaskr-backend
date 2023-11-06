from typing import TypeVar

from sqlalchemy import or_

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Role, RoleType

TRoleTypeQueryset = TypeVar("TRoleTypeQueryset", bound="RoleTypeQueryset")


class RoleTypeQueryset(Queryset):
    def __init__(self):
        super().__init__(RoleType)

    def user_have(self, user_id: str) -> TRoleTypeQueryset:
        self._query = self._query.join(Role).where(Role.user_id == user_id)
        return self

    def user_can_use(self, group_ids: list[str]) -> TRoleTypeQueryset:
        self._query = self._query.where(
            or_(
                RoleType.group_id.in_(group_ids),
                RoleType.group_id == None,  # noqa E711
                RoleType.group_id == "",
            )
        )
        return self

    def user_can_modify(self, group_ids: list[str]) -> TRoleTypeQueryset:
        self._query = self._query.where(RoleType.group_id.in_(group_ids))
        return self
