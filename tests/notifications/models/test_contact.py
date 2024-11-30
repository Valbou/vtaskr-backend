from datetime import datetime
from unittest import TestCase

from babel import Locale
from faker import Faker

from src.notifications.models import Contact


class TestContact(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.contact = Contact(
            first_name="first",
            last_name="last",
            email="text@example.com",
        )

    def test_table_fields(self):
        self.assertEqual(Contact.__annotations__.get("first_name"), str)
        self.assertEqual(Contact.__annotations__.get("last_name"), str)
        self.assertEqual(Contact.__annotations__.get("timezone"), str | None)
        self.assertEqual(Contact.__annotations__.get("locale"), Locale | None)
        self.assertEqual(Contact.__annotations__.get("email"), str)
        self.assertEqual(Contact.__annotations__.get("telegram"), str)
        self.assertEqual(Contact.__annotations__.get("phone_number"), str)
        self.assertEqual(Contact.__annotations__.get("id"), str | None)
        self.assertEqual(Contact.__annotations__.get("updated_at"), datetime | None)
        self.assertEqual(Contact.__annotations__.get("created_at"), datetime | None)
