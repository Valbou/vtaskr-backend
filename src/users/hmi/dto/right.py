from dataclasses import dataclass

from src.libs.iam.constants import Permissions
from src.libs.openapi.base import openapi
from src.users.models import Right

RIGHT_COMPONENT = "#/components/schemas/Right"

right_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "roletype_id": {"type": "string"},
        "resource": {"type": "string"},
        "permissions": {"type": "integer"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["roletype_id", "resource", "permissions"],
}
openapi.register_schemas_components("Right", right_component)


@dataclass
class RightDTO:
    id: str = ""
    roletype_id: str = ""
    resource: str = ""
    permissions: int = 0
    created_at: str = ""


class RightMapperDTO:
    @classmethod
    def model_to_dto(cls, right: Right) -> RightDTO:
        return RightDTO(
            id=right.id,
            roletype_id=right.roletype_id,
            resource=right.resource,
            permissions=sum([perm.value for perm in right.permissions]),
            created_at=right.created_at.isoformat(),
        )

    @classmethod
    def dto_to_model(cls, right_dto: RightDTO, right: Right | None = None) -> Right:
        if not right:
            right = Right(
                roletype_id=right_dto.roletype_id,
                resource=right_dto.resource,
                permissions=[
                    perm for perm in Permissions if right_dto.permissions & perm
                ],
            )

        else:
            right.roletype_id = right_dto.roletype_id
            right.resource = right_dto.resource
            right.permissions = [
                perm for perm in Permissions if right_dto.permissions & perm
            ]

        return right
