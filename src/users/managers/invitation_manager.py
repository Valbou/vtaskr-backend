from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions
from src.users.models import Invitation
from src.users.persistence import InvitationDBPort
from src.users.settings import APP_NAME


class InvitationManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.invitation_db: InvitationDBPort = self.services.persistence.get_repository(
            APP_NAME, "Invitation"
        )

    def clean_expired(self, session) -> None:
        """Clean invitation expired"""

        self.invitation_db.clean_expired(session=session)

    def get_invitation(self, session, invitation_id: str) -> Invitation | None:
        return self.invitation_db.load(session=session, id=invitation_id)

    def get_from_hash(self, session, hash: str) -> Invitation | None:
        """Retrieve invitation from hash"""

        return self.invitation_db.get_from_hash(session=session, hash=hash)

    def get_from_group(self, session, user_id: str, group_id: str) -> list[Invitation]:
        """Get invitations associated with a group"""

        if self.services.identity.can(
            session=session,
            permission=Permissions.READ,
            user_id=user_id,
            group_id_resource=group_id,
            resource="Group",
        ):
            return self.invitation_db.get_from_group(session=session, group_id=group_id)

        return []

    def update_invitation(self, session, user_id: str, invitation: Invitation) -> bool:
        """Create or update an invitation"""

        if user_id and self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            invitation.in_group_id,
            resource="Group",
        ):
            self.invitation_db.save(session=session, obj=invitation)

            return True

        return False

    def delete_invitation(self, session, user_id: str, invitation: Invitation) -> bool:
        """Delete an invitation"""

        if self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            invitation.in_group_id,
            resource="Group",
        ):
            self.invitation_db.delete(session=session, obj=invitation)

            return True

        return False

    def delete_invitation_by_id(
        self, session, user_id: str, group_id: str, invitation_id: str
    ) -> bool:
        """Delete an invitation from an id"""

        if self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            group_id,
            resource="Group",
        ):
            self.invitation_db.delete_by_id(session=session, id=invitation_id)

            return True

        return False
