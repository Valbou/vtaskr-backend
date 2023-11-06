from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.users.models import Group

GROUP_COMPONENT = "#/components/schemas/Group"

group_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["name"],
}
openapi.register_schemas_components("Group", group_component)


@dataclass
class GroupDTO:
    id: str = ""
    name: str = ""
    created_at: str = ""


class GroupMapperDTO:
    @classmethod
    def model_to_dto(cls, group: Group) -> GroupDTO:
        return GroupDTO(
            id=group.id,
            name=group.name,
            created_at=group.created_at.isoformat(),
        )

    @classmethod
    def dto_to_model(cls, group_dto: GroupDTO, group: Group | None = None) -> Group:
        if not group:
            group = Group(name=group_dto.name)
        else:
            group.name = group_dto.name

        return group
