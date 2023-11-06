from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.users.models import Role

ROLE_COMPONENT = "#/components/schemas/Role"

role_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "user_id": {"type": "string"},
        "group_id": {"type": "string"},
        "roletype_id": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["user_id", "group_id", "roletype_id"],
}
openapi.register_schemas_components("Role", role_component)


@dataclass
class RoleDTO:
    id: str = ""
    user_id: str = ""
    group_id: str = ""
    roletype_id: str = ""
    created_at: str = ""


class RoleMapperDTO:
    @classmethod
    def model_to_dto(cls, role: Role) -> RoleDTO:
        return RoleDTO(
            id=role.id,
            user_id=role.user_id,
            group_id=role.group_id,
            roletype_id=role.roletype_id,
            created_at=role.created_at.isoformat(),
        )

    @classmethod
    def dto_to_model(cls, role_dto: RoleDTO, role: Role | None = None) -> Role:
        if not role:
            role = Role(
                user_id=role_dto.user_id,
                group_id=role_dto.group_id,
                roletype_id=role_dto.roletype_id,
            )

        else:
            role.user_id = role_dto.user_id
            role.group_id = role_dto.group_id
            role.roletype_id = role_dto.roletype_id

        return role
