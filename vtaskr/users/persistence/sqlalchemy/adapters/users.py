from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.libs.sqlalchemy.default_adapter import DefaultDB
from vtaskr.users.models import Right, Role, RoleType, User
from vtaskr.users.persistence.ports import AbstractUserPort
from vtaskr.users.persistence.sqlalchemy.querysets import UserQueryset


class UserDB(AbstractUserPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = UserQueryset()

    def update(self, session: Session, user: User, autocommit: bool = True):
        self.qs.update().id(user.id).values(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hash_password=user.hash_password,
        )

        session.execute(self.qs.statement)
        if autocommit:
            session.commit()

    def find_login(self, session: Session, email: str) -> Optional[User]:
        self.qs.by_email(email)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def clean_unused(self, session: Session, autocommit: bool = True):
        self.qs.delete().unused()
        session.execute(self.qs.statement)

        if autocommit:
            session.commit()

    def has_permissions(
        self,
        session: Session,
        id: str,
        resource: Resources,
        permission: Permissions,
        group_id: str,
    ) -> bool:
        self.qs.join(User.roles).join(Role.roletype).join(RoleType.rights).where(
            Role.group_id == group_id,
            Right.resource == resource,
            Right.permissions.bitwise_and(permission) > 0,
        ).id(id)

        return session.query(self.qs.statement.exists()).scalar()
