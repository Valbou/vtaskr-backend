from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.notifications.models import Contact, MessageType, Subscription


class TestSubscription(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Subscription(
            type=MessageType.SMS,
            name="test",
            contact_id="1234abcd",
            contact=Contact(
                first_name="first_name",
                last_name="last_name",
                email="text@example.com",
            ),
        )

    def test_table_fields(self):
        self.assertEqual(Subscription.__annotations__.get("type"), MessageType)
        self.assertEqual(Subscription.__annotations__.get("name"), str)
        self.assertEqual(Subscription.__annotations__.get("contact_id"), str)
        self.assertEqual(Subscription.__annotations__.get("contact"), Contact)
        self.assertEqual(Subscription.__annotations__.get("id"), str | None)
        self.assertEqual(Subscription.__annotations__.get("updated_at"), datetime | None)
        self.assertEqual(Subscription.__annotations__.get("created_at"), datetime | None)
