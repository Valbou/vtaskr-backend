from unittest import TestCase

from faker import Faker

from src.notifications.models import Subscription
from src.ports import MessageType


class TestSubscription(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Subscription(
            event_type=MessageType.SMS,
            event_name="test",
            tenant_id="1234abcd",
            to="test@example.com",
        )

    def test_user_table_fields(self):
        self.assertEqual(Subscription.__annotations__.get("event_type"), MessageType)
        self.assertEqual(Subscription.__annotations__.get("event_name"), str)
        self.assertEqual(Subscription.__annotations__.get("tenant_id"), str)
        self.assertEqual(Subscription.__annotations__.get("to"), str)
        self.assertEqual(Subscription.__annotations__.get("cc"), str)
        self.assertEqual(Subscription.__annotations__.get("bcc"), str)
