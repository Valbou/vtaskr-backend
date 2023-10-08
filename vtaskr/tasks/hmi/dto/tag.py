from dataclasses import asdict, dataclass
from typing import Optional

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
}
openapi.register_schemas_components("Tag", tag_component)


@dataclass
class TagDTO:
    id: Optional[str] = ""
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
    def list_models_to_list_dto(cls, tags: list[Tag] | None) -> list[TagDTO] | None:
        return [TagMapperDTO.model_to_dto(t) for t in tags] if tags else None

    @classmethod
    def dto_to_model(cls, tag_dto: TagDTO, tag: Optional[Tag] = None) -> Tag:
        if not tag:
            tag = Tag(tenant_id=tag_dto.tenant_id, title=tag_dto.title)

        tag.title = tag_dto.title
        tag.color = Color(tag_dto.backgound_color, tag_dto.text_color)

        return tag

    @classmethod
    def dto_to_dict(cls, tag_dto: TagDTO) -> dict:
        return asdict(tag_dto)

    @classmethod
    def list_dto_to_dict(cls, tags_dto: list[TagDTO]) -> list[dict]:
        return [asdict(tag_dto) for tag_dto in tags_dto]
