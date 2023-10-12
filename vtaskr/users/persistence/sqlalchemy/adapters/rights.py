from sqlalchemy.orm import Session

from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.models import Right
from vtaskr.users.persistence.ports import AbstractRightPort
from vtaskr.users.persistence.sqlalchemy.querysets import RightQueryset


class RightDB(AbstractRightPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RightQueryset()

    def get_all_user_rights(
        self, session: Session, user_id: str, group_ids: list[str]
    ) -> list[Right]:
        self.qs.select().both_user_have_and_user_can_use(group_ids=group_ids)

        return session.scalars(self.qs.statement).all()

    def get_a_user_right(
        self, session: Session, user_id: str, right_id: str, group_ids: list[str]
    ) -> Right | None:
        self.qs.select().both_user_have_and_user_can_use(group_ids=group_ids).id(
            right_id
        )

        return session.scalars(self.qs.statement).one_or_none()
