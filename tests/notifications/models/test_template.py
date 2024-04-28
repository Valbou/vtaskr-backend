from unittest import TestCase

from faker import Faker

from src.notifications.models import Template
from src.ports import MessageType


class TestTemplate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = Template(
            event_type=MessageType.SMS,
            event_name="test",
            sender="test@example.com",
        )

    def test_user_table_fields(self):
        self.assertEqual(Template.__annotations__.get("event_type"), MessageType)
        self.assertEqual(Template.__annotations__.get("event_name"), str)
        self.assertEqual(Template.__annotations__.get("sender"), str)
        self.assertEqual(Template.__annotations__.get("name"), str)
        self.assertEqual(Template.__annotations__.get("subject"), str)
        self.assertEqual(Template.__annotations__.get("html"), str)
        self.assertEqual(Template.__annotations__.get("text"), str)

    event_type: MessageType
    event_name: str
    sender: str
    name: str = ""
    subject: str = ""
    html: str = ""
    text: str = ""
