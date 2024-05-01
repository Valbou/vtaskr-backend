from unittest import TestCase

from faker import Faker

from src.notifications.models import Subscription, Contact
from src.ports import MessageType


class TestSubscription(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Subscription(
            event_type=MessageType.SMS,
            event_name="test",
            contact_id="1234abcd",
            contact=Contact(
                id="1234abcd",
                email="text@example.com",
            )
        )

    def test_table_fields(self):
        self.assertEqual(Subscription.__annotations__.get("event_type"), MessageType)
        self.assertEqual(Subscription.__annotations__.get("event_name"), str)
        self.assertEqual(Subscription.__annotations__.get("contact_id"), str)
