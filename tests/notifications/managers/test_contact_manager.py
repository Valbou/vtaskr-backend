from unittest.mock import MagicMock

from src.notifications.managers import ContactManager
from src.notifications.models import Contact
from tests.base_test import DummyBaseTestCase


class TestContactManager(DummyBaseTestCase):
    def setUp(self):
        super().setUp()

        self.manager = ContactManager(services=self.app.dependencies)

    def get_contact(self) -> Contact:
        return Contact(
            first_name="first",
            last_name="last",
            email="test@example.com",
        )

    def get_by_id(self):
        self.manager.contact_db.load = MagicMock()
        self.manager.get_by_id(session=None, contact_id="abc123")
        self.manager.contact_db.load.assert_called_once()

    def create(self):
        contact = self.get_contact()
        self.manager.contact_db.save = MagicMock()
        self.manager.create(session=None, contact=contact)
        self.manager.contact_db.save.assert_called_once()

    def update(self):
        contact = self.get_contact()
        self.manager.contact_db.update = MagicMock()
        self.manager.update(session=None, contact=contact)
        self.manager.contact_db.update.assert_called_once()

    def delete(self):
        contact = self.get_contact()
        self.manager.contact_db.delete = MagicMock()
        self.manager.delete(session=None, contact=contact)
        self.manager.contact_db.delete.assert_called_once()
