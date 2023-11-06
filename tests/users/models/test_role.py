from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.colors.models.color import Color
from src.users import Role


class TestRole(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Role(
            user_id=self.fake.word(),
            group_id=self.fake.word(),
            roletype_id=self.fake.word(),
        )

    def test_user_table_fields(self):
        self.assertEqual(Role.__annotations__.get("id"), str | None)
        self.assertEqual(Role.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(Role.__annotations__.get("user_id"), str)
        self.assertEqual(Role.__annotations__.get("group_id"), str)
        self.assertEqual(Role.__annotations__.get("roletype_id"), str)
        self.assertEqual(Role.__annotations__.get("color"), Color | None)
