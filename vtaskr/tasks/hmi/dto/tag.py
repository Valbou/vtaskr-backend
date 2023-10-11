from dataclasses import dataclass

from vtaskr.libs.openapi.base import openapi
from vtaskr.tasks.models import Color, Tag

tag_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "tenant_id": {"type": "string"},
        "title": {"type": "string"},
        "backgound_color": {"type": "string"},
        "text_color": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "required": [
        "tenant_id", "title"
    ],
}
openapi.register_schemas_components("Tag", tag_component)


@dataclass
class TagDTO:
    id: str | None = ""
    created_at: str = ""
    tenant_id: str = ""
    title: str = ""
    backgound_color: str = "#000000"
    text_color: str = "#FFFFFF"


class TagMapperDTO:
    @classmethod
    def model_to_dto(cls, tag: Tag) -> TagDTO:
        return TagDTO(
            id=tag.id,
            created_at=tag.created_at.isoformat(),
            tenant_id=tag.tenant_id,
            title=tag.title,
            backgound_color=tag.color.background,
            text_color=tag.color.text,
        )

    @classmethod
    def dto_to_model(cls, tag_dto: TagDTO, tag: Tag | None = None) -> Tag:
        if not tag:
            tag = Tag(tenant_id=tag_dto.tenant_id, title=tag_dto.title)

        tag.title = tag_dto.title
        tag.color = Color(tag_dto.backgound_color, tag_dto.text_color)

        return tag
