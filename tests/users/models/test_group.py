from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.users import Group


class TestGroup(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Group(
            name=self.fake.word(),
        )

    def test_user_table_fields(self):
        self.assertEqual(Group.__annotations__.get("id"), str | None)
        self.assertEqual(Group.__annotations__.get("name"), str)
        self.assertEqual(Group.__annotations__.get("created_at"), datetime | None)
