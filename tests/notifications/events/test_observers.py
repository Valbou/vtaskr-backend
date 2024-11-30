from unittest.mock import MagicMock, patch

from src.notifications.events import (
    UsersDeleteUserObserver,
    UsersRegisterUserObserver,
    UsersUpdateUserObserver,
)
from src.notifications.models import Contact
from tests.base_test import DummyBaseTestCase


class TestObservers(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.repository_mock = MagicMock()
        self.app.dependencies.persistence.get_repository = MagicMock(
            return_value=self.repository_mock
        )

    def test_users_register_user(self):
        event_data = {
            "tenant_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "",
            "phone_number": "",
        }

        with patch(
            "src.notifications.events.users.users_observers.NotificationService"
        ) as MockClass:
            service = MockClass.return_value
            service.add_new_contact.return_value = MagicMock()
            service.add_messages.return_value = MagicMock()
            service.build_messages.return_value = MagicMock()
            service.notify_all.return_value = MagicMock()

            UsersRegisterUserObserver.run(
                self.app, event_name="users:register:user", event_data=event_data
            )

            service.add_new_contact.assert_called_once()
            service.build_messages.assert_called_once()
            service.add_messages.assert_called_once()
            service.notify_all.assert_called_once()

    def test_1_update_existing_user_observer(self):
        contact = Contact(
            id="abc123",
            first_name="first",
            last_name="last",
            email=self.generate_email(),
            telegram="",
            phone_number="",
        )

        event_data = {
            "tenant_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        self.repository_mock.load.return_value = contact

        UsersUpdateUserObserver.run(
            self.app, event_name="users:update:user", event_data=event_data
        )

        self.repository_mock.update.assert_called_once()
        self.repository_mock.save.assert_not_called()
        self.assertEqual(contact.email, event_data.get("email"))
        self.assertEqual(contact.telegram, event_data.get("telegram"))
        self.assertEqual(contact.phone_number, event_data.get("phone_number"))

    def test_1_update_missing_user_observer(self):
        event_data = {
            "tenant_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        self.repository_mock.load.return_value = None

        UsersUpdateUserObserver.run(
            self.app, event_name="users:update:user", event_data=event_data
        )

        self.repository_mock.save.assert_called_once()
        self.repository_mock.update.assert_not_called()

    def test_2_delete_user_observer(self):
        event_data = {
            "tenant_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        UsersDeleteUserObserver.run(
            self.app, event_name="users:delete:user", event_data=event_data
        )

        self.repository_mock.delete_by_id.assert_called_once()
