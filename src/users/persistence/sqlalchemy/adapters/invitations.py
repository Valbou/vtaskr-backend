from sqlalchemy.orm import Session

from src.libs.sqlalchemy.default_adapter import DefaultDB
from src.users.models import Invitation
from src.users.persistence.ports import InvitationDBPort
from src.users.persistence.sqlalchemy.querysets import InvitationQueryset


class InvitationDB(InvitationDBPort, DefaultDB):
    def __init__(self) -> None:
        super().__init__()
        self.qs = InvitationQueryset()

    def clean_expired(self, session: Session):
        self.qs.delete().expired()
        session.execute(self.qs.statement)

    def get_from_hash(self, session, hash: str) -> Invitation | None:
        self.qs.select().where(Invitation.hash == hash)
        invitation = session.scalars(self.qs.statement).one_or_none()
        return invitation

    def get_from_group(self, session, group_id: str) -> list[Invitation]:
        self.qs.select().where(Invitation.in_group_id == group_id)
        invitations = session.scalars(self.qs.statement).all()
        return invitations
