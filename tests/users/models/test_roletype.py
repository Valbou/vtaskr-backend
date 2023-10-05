from datetime import datetime
from typing import Optional
from unittest import TestCase

from faker import Faker

from vtaskr.users import RoleType


class TestRoleType(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = RoleType(
            name=self.fake.word(),
            group_id=self.fake.word(),
        )

    def test_user_table_fields(self):
        self.assertEqual(RoleType.__annotations__.get("id"), str)
        self.assertEqual(RoleType.__annotations__.get("created_at"), datetime)
        self.assertEqual(RoleType.__annotations__.get("name"), str)
        self.assertEqual(RoleType.__annotations__.get("group_id"), Optional[str])
