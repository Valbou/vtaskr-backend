from unittest import TestCase

from faker import Faker

from src.notifications.models import Contact


class TestContact(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.contact = Contact(
            id="1234abcd",
            email="text@example.com",
        )

    def test_table_fields(self):
        self.assertEqual(Contact.__annotations__.get("email"), str)
        self.assertEqual(Contact.__annotations__.get("telegram"), str)
        self.assertEqual(Contact.__annotations__.get("phone_number"), str)
