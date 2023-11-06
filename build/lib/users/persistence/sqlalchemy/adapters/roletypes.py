from sqlalchemy.orm import Session

from src.libs.flask.querystring import Filter
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import RoleType
from src.users.persistence.ports import AbstractRoleTypePort
from src.users.persistence.sqlalchemy.querysets import RoleTypeQueryset


class RoleTypeDB(AbstractRoleTypePort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = RoleTypeQueryset()

    def get_or_create(
        self, session: Session, roletype: RoleType
    ) -> tuple[RoleType, bool]:
        self.qs.select().where(
            RoleType.name == roletype.name, RoleType.group_id == roletype.group_id
        )
        roletype_from_db = session.scalars(self.qs.statement).one_or_none()

        created = False
        if not roletype_from_db:
            self.save(session, roletype)
            roletype_from_db = roletype
            created = True

        return (roletype_from_db, created)

    def get_a_user_roletype(
        self, session: Session, roletype_id: str, group_ids: list[str]
    ) -> RoleType:
        self.qs.select().user_can_use(group_ids=group_ids).id(roletype_id)

        return session.scalars(self.qs.statement).one_or_none()

    def get_all_user_roletypes(
        self,
        session: Session,
        group_ids: list[str],
        filters: list[Filter] | None = None,
    ) -> list[RoleType]:
        filters = filters or []
        if filters:
            self.qs.from_filters(filters)

        self.qs.select().user_can_use(group_ids=group_ids)

        return session.scalars(self.qs.statement).all()
