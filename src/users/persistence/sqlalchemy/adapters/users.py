from sqlalchemy.orm import Session

from src.libs.iam.constants import Permissions
from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Right, Role, RoleType, User
from src.users.persistence.ports import UserDBPort
from src.users.persistence.sqlalchemy.querysets import UserQueryset


class UserDB(UserDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = UserQueryset()

    def update(self, session: Session, user: User):
        self.qs.update().id(user.id).values(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hash_password=user.hash_password,
        )
        session.execute(self.qs.statement)

    def find_user_by_email(self, session: Session, email: str) -> User | None:
        self.qs.select().by_email(email)
        result = session.scalars(self.qs.statement).one_or_none()
        return result

    def clean_unused(self, session: Session):
        self.qs.delete().unused()
        session.execute(self.qs.statement)

    def has_permissions(
        self,
        session: Session,
        id: str,
        resource: str,
        permission: Permissions,
        group_id: str,
    ) -> bool:
        self.qs.select().join(User.roles).join(Role.roletype).join(
            RoleType.rights
        ).where(
            Role.group_id == group_id,
            Right.resource == resource,
            Right.permissions.bitwise_and(permission) > 0,
        ).id(
            id
        )

        return session.query(self.qs.statement.exists()).scalar()
