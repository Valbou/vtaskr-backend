from unittest import TestCase

from src.tasks.hmi.dto import Tag, TagDTO, TagMapperDTO


class TagMapperTest(TestCase):
    def test_mapper_model_to_dto(self):
        tag = Tag(title="My tag", tenant_id="abc123")

        tag_dto = TagMapperDTO.model_to_dto(tag=tag)

        self.assertIsInstance(tag_dto, TagDTO)

    def test_mapper_dto_to_model(self):
        tag_dto = TagDTO(
            title="My tag",
            tenant_id="abc123",
        )

        tag = TagMapperDTO.dto_to_model(tag_dto=tag_dto)

        self.assertIsInstance(tag, Tag)
