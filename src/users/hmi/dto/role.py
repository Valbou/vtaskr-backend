from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.users.hmi.dto import GROUP_COMPONENT, ROLETYPE_COMPONENT, USER_COMPONENT
from src.users.models import Group, Role, RoleType, User

ROLE_COMPONENT = "#/components/schemas/Role"

role_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "user_id": {"type": "string"},
        "user": {"$ref": USER_COMPONENT},
        "group_id": {"type": "string"},
        "group": {"$ref": GROUP_COMPONENT},
        "roletype_id": {"type": "string"},
        "roletype": {"$ref": ROLETYPE_COMPONENT},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": ["user_id", "group_id", "roletype_id"],
}
openapi.register_schemas_components("Role", role_component)


@dataclass
class RoleDTO:
    id: str = ""
    user_id: str = ""
    user: User | None = None
    group_id: str = ""
    group: Group | None = None
    roletype_id: str = ""
    roletype: RoleType | None = None
    created_at: str = ""


class RoleMapperDTO:
    @classmethod
    def model_to_dto(cls, role: Role) -> RoleDTO:
        from src.users.hmi.dto import GroupMapperDTO, RoleTypeMapperDTO, UserMapperDTO

        user_dto = UserMapperDTO().model_to_dto(role.user) if role.user else None
        group_dto = GroupMapperDTO().model_to_dto(role.group) if role.group else None
        roletype_dto = (
            RoleTypeMapperDTO().model_to_dto(role.roletype) if role.roletype else None
        )

        return RoleDTO(
            id=role.id,
            user_id=role.user_id,
            user=user_dto,
            group_id=role.group_id,
            group=group_dto,
            roletype_id=role.roletype_id,
            roletype=roletype_dto,
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
