from dataclasses import dataclass

from vtaskr.libs.openapi.base import openapi
from vtaskr.users.models import Group

group_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
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

        group.name = group_dto.first_name
        return group
