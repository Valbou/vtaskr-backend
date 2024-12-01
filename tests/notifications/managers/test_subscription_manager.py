from unittest.mock import MagicMock

from src.notifications.managers import SubscriptionManager
from src.notifications.models import Contact, Subscription
from src.notifications.settings import MessageType
from tests.base_test import DummyBaseTestCase


class TestSubscriptionManager(DummyBaseTestCase):
    def setUp(self):
        super().setUp()

        self.manager = SubscriptionManager(services=self.app.dependencies)

    def get_contact(self) -> Contact:
        return Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )

    def get_subscriptions(self, contact: Contact, number: int) -> list[Subscription]:
        return [
            Subscription(
                type=MessageType.EMAIL,
                name=self.fake.word(),
                contact_id=contact.id,
                contact=contact,
            )
            for _ in range(number)
        ]

    def test_subscribe(self):
        contact = self.get_contact()
        self.manager.subscription_db.save = MagicMock()

        self.manager.subscribe(
            session=None, name="test", type=MessageType.EMAIL, contact=contact
        )

        self.manager.subscription_db.save.assert_called_once()

    def test_create(self):
        self.manager.subscription_db.save = MagicMock()

        self.manager.create(session=None, subscription=None)

        self.manager.subscription_db.save.assert_called_once()

    def test_get_subscriptions_indexed_by_message_type(self):
        contact = self.get_contact()
        number = 3
        subscriptions = self.get_subscriptions(contact=contact, number=number)

        index = self.manager.get_subscriptions_indexed_by_message_type(
            subscriptions=subscriptions
        )

        self.assertIsInstance(index, dict)
        self.assertEqual(len(index[MessageType.EMAIL.name]), number)

    def get_subscriptions_for_event(self) -> list[Subscription]:
        contact = self.get_contact()
        number = 3
        subscriptions = self.get_subscriptions(contact=contact, number=number)

        self.manager.subscription_db.get_subscriptions_for_event = MagicMock(
            return_value=subscriptions
        )

        self.manager.get_subscriptions_for_event(
            session=None, name="test", targets=["foo", "bar"]
        )

        self.manager.subscription_db.get_subscriptions_for_event.assert_called_once()
