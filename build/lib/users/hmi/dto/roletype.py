from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.users.models import RoleType

ROLETYPE_COMPONENT = "#/components/schemas/RoleType"

roletype_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "group_id": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["name"],
}
openapi.register_schemas_components("RoleType", roletype_component)


@dataclass
class RoleTypeDTO:
    id: str = ""
    name: str = ""
    group_id: str = ""
    created_at: str = ""


class RoleTypeMapperDTO:
    @classmethod
    def model_to_dto(cls, roletype: RoleType) -> RoleTypeDTO:
        return RoleTypeDTO(
            id=roletype.id,
            name=roletype.name,
            group_id=roletype.group_id,
            created_at=roletype.created_at.isoformat(),
        )

    @classmethod
    def dto_to_model(cls, roletype_dto: RoleTypeDTO, roletype: RoleType) -> RoleType:
        roletype.name = roletype_dto.name

        return roletype
