from typing import Self

from sqlalchemy import or_

from src.libs.sqlalchemy.queryset import Queryset
from src.users.models import Role


class RoleQueryset(Queryset):
    def __init__(self):
        super().__init__(Role)

    def is_mine(self, user_id: str) -> Self:
        self._query = self._query.where(self.qs_class.user_id == user_id)
        return self

    def is_under_my_control(self, group_ids: list[str]) -> Self:
        self._query = self._query.where(self.qs_class.group_id.in_(group_ids))
        return self

    def both_is_mine_and_is_under_my_control(
        self, user_id: str, group_ids: list[str]
    ) -> Self:
        self._query = self._query.where(
            or_(self.qs_class.user_id == user_id, self.qs_class.group_id.in_(group_ids))
        )
        return self

    def group_roles(self, group_id: str) -> Self:
        self._query = self._query.where(self.qs_class.group_id == group_id)
        return self
