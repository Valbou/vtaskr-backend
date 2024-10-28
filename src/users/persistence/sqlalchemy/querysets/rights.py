from typing import Self

from sqlalchemy import or_

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Right, Role, RoleType


class RightQueryset(Queryset):
    def __init__(self):
        super().__init__(Right)

    def user_have(self, user_id: str) -> Self:
        self._query = (
            self._query.join(Right.roletype).join(Role).where(Role.user_id == user_id)
        )
        return self

    def user_can_use(self, group_ids: list[str]) -> Self:
        self._query = self._query.join(Right.roletype).where(
            or_(
                RoleType.group_id.in_(group_ids),
                RoleType.group_id == None,  # noqa E711
                RoleType.group_id == "",
            )
        )
        return self

    def both_user_have_and_user_can_use(self, group_ids: list[str]) -> Self:
        self._query = self._query.join(Right.roletype).where(
            or_(
                RoleType.group_id.in_(group_ids),
                RoleType.group_id == None,  # noqa E711
                RoleType.group_id == "",
            )
        )
        return self

    def all_roletype_rights(self, roletype_id: str) -> Self:
        self._query = self._query.where(Role.roletype_id == roletype_id)

        return self
