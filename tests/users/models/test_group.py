from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.users.models import Group


class TestGroup(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.group = Group(
            name=self.fake.word(),
            is_private=False,
        )

    def test_table_fields(self):
        self.assertEqual(Group.__annotations__.get("id"), str | None)
        self.assertEqual(Group.__annotations__.get("name"), str)
        self.assertEqual(Group.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(Group.__annotations__.get("is_private"), bool)
