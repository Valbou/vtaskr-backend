from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.libs.iam.constants import Permissions, Resources
from src.users import Right


class TestRight(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Right(
            roletype_id=self.fake.word(),
            resource=Resources.TASK,
            permissions=Permissions.CREATE,
        )

    def test_table_fields(self):
        self.assertEqual(Right.__annotations__.get("id"), str | None)
        self.assertEqual(Right.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(Right.__annotations__.get("roletype_id"), str)
        self.assertEqual(Right.__annotations__.get("resource"), Resources)
        self.assertEqual(
            Right.__annotations__.get("permissions"), list[Permissions] | None
        )
