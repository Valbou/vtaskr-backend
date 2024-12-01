from unittest.mock import MagicMock, patch

from src.notifications.events import (
    UsersDeleteUserObserver,
    UsersRegisterUserObserver,
    UsersUpdateUserObserver,
)
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
            "user_id": "abc123",
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

    def test_update_existing_user_observer(self):
        event_data = {
            "user_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        with patch(
            "src.notifications.events.users.users_observers.NotificationService"
        ) as MockClass:
            service = MockClass.return_value
            service.update_contact = MagicMock()

            UsersUpdateUserObserver.run(
                self.app, event_name="users:update:user", event_data=event_data
            )

            service.update_contact.assert_called_once()

    def test_delete_user_observer(self):
        event_data = {
            "user_id": "abc123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        with patch(
            "src.notifications.events.users.users_observers.NotificationService"
        ) as MockClass:
            service = MockClass.return_value
            service.delete_contact = MagicMock()

            UsersDeleteUserObserver.run(
                self.app, event_name="users:delete:user", event_data=event_data
            )

            service.delete_contact.assert_called_once()
