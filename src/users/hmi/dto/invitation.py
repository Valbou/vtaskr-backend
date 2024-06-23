from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.users.models import Invitation

INVITATION_COMPONENT = "#/components/schemas/Invitation"

invitation_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "from_user_id": {"type": "string"},
        "to_user_email": {"type": "string"},
        "in_group_id": {"type": "string"},
        "with_roletype_id": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["from_user_id", "to_user_email", "in_group_id", "with_roletype_id"],
}
openapi.register_schemas_components("Invitation", invitation_component)


@dataclass
class InvitationDTO:
    id: str = ""
    from_user_id: str = ""
    to_user_email: str = ""
    in_group_id: str = ""
    with_roletype_id: str = ""
    created_at: str = ""


class InvitationMapperDTO:
    @classmethod
    def model_to_dto(cls, invitation: Invitation) -> InvitationDTO:
        return InvitationDTO(
            id=invitation.id,
            from_user_id=invitation.from_user_id,
            to_user_email=invitation.to_user_email,
            in_group_id=invitation.in_group_id,
            with_roletype_id=invitation.with_roletype_id,
            created_at=invitation.created_at.isoformat(),
        )

    @classmethod
    def dto_to_model(
        cls, invitation_dto: InvitationDTO, invitation: Invitation | None = None
    ) -> Invitation:
        if not invitation:
            invitation = Invitation(
                from_user_id=invitation_dto.from_user_id,
                to_user_email=invitation_dto.to_user_email,
                in_group_id=invitation_dto.in_group_id,
                with_roletype_id=invitation_dto.with_roletype_id,
            )

        else:
            invitation.from_user_id = invitation_dto.from_user_id
            invitation.to_user_email = invitation_dto.to_user_email
            invitation.in_group_id = invitation_dto.in_group_id
            invitation.with_roletype_id = invitation_dto.with_roletype_id

        return invitation
