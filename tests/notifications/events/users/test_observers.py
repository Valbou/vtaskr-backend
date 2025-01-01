from datetime import datetime
from unittest.mock import MagicMock, patch

from src.notifications.events import (
    UsersChangeEmailObserver,
    UsersDeleteUserObserver,
    UsersInviteUserObserver,
    UsersNotificationsObserver,
    UsersRegisterUserObserver,
    UsersUpdateUserObserver,
)
from tests.base_test import DummyBaseTestCase

NOTIFICATION_SERVICE_PATH = (
    "src.notifications.events.users.users_observers.NotificationService"
)


class TestUsersNotificationsObservers(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.repository_mock = MagicMock()
        self.app.dependencies.persistence.get_repository = MagicMock(
            return_value=self.repository_mock
        )

    def test_users_register_user(self):
        event_data = {
            "user_id": "user_123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "",
            "phone_number": "",
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
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
            "user_id": "user_123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.update_contact = MagicMock()

            UsersUpdateUserObserver.run(
                self.app, event_name="users:update:user", event_data=event_data
            )

            service.update_contact.assert_called_once()

    def test_delete_user_observer(self):
        event_data = {
            "user_id": "user_123",
            "first_name": "first",
            "last_name": "last",
            "email": self.generate_email(),
            "telegram": "123456",
            "phone_number": "654321",
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.delete_contact = MagicMock()

            UsersDeleteUserObserver.run(
                self.app, event_name="users:delete:user", event_data=event_data
            )

            service.delete_contact.assert_called_once()

    def test_change_email_observer(self):
        event_data = {
            "targets": ["user_123"],
            "user_id": "user_123",
            "email": "old@example.com",
            "new_email": "new@example.com",
            "first_name": "first",
            "last_name": "last",
            "hash": "hash_123",
            "code": "1234",
            "valid_until": datetime.now().isoformat(),
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.build_messages = MagicMock(return_value=["a"])
            service.add_new_contact = MagicMock()
            service.add_messages = MagicMock()
            service.notify_all = MagicMock()

            UsersChangeEmailObserver.run(
                self.app, event_name="users:change_email:user", event_data=event_data
            )

            self.assertEqual(service.build_messages.call_count, 2)
            service.add_new_contact.assert_called_once()
            service.add_messages.assert_called_once_with(messages=["a", "a"])
            service.notify_all.assert_called_once()

    def test_notifications_observer(self):
        event_data = {
            "targets": ["user_123"],
            "email": "test@example.com",
            "first_name": "first",
            "last_name": "last",
            "code": "1234",
            "valid_until": datetime.now().isoformat(),
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.build_messages = MagicMock(return_value=["a"])
            service.add_messages = MagicMock()
            service.notify_all = MagicMock()

            UsersNotificationsObserver.run(
                self.app, event_name="users:login_2fa:user", event_data=event_data
            )

            service.build_messages.assert_called_once()
            service.add_messages.assert_called_once_with(messages=["a"])
            service.notify_all.assert_called_once()

    def test_invite_user_observer(self):
        event_data = {
            "targets": ["user_123"],
            "from_name": "first last",
            "timezone": "UTC",
            "locale": "en_GB",
            "group_name": "Group",
            "role_name": "Roletype",
            "invited_email": "unknown@example.com",
            "hash": "hash_123",
            "valid_until": datetime.now().isoformat(),
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.add_new_contact = MagicMock()
            service.build_messages = MagicMock(return_value=["a"])
            service.add_messages = MagicMock()
            service.notify_all = MagicMock()
            service.delete_contact = MagicMock()

            UsersInviteUserObserver.run(
                self.app, event_name="users:invite:user", event_data=event_data
            )

            service.add_new_contact.assert_called_once()
            service.build_messages.assert_called_once()
            service.add_messages.assert_called_once_with(messages=["a"])
            service.notify_all.assert_called_once()
            service.delete_contact.assert_called_once()
