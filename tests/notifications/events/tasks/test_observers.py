from unittest.mock import MagicMock, patch

from src.notifications.events import TasksNotificationsObserver
from tests.base_test import DummyBaseTestCase

NOTIFICATION_SERVICE_PATH = (
    "src.notifications.events.tasks.tasks_observers.NotificationService"
)


class TestTasksNotificationsObserver(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.repository_mock = MagicMock()
        self.app.dependencies.persistence.get_repository = MagicMock(
            return_value=self.repository_mock
        )

    def test_notifications_observer(self):
        event_data = {
            "targets": ["assigned_123"],
            "user_id": "assigned_123",
            "today": [],
            "nb_today": 0,
            "tomorrow": [],
            "nb_tomorrow": 0,
        }

        with patch(NOTIFICATION_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.build_messages = MagicMock(return_value=["a"])
            service.add_messages = MagicMock()
            service.notify_all = MagicMock()

            TasksNotificationsObserver.run(
                self.app, event_name="tasks:todo_today:tasks", event_data=event_data
            )

            service.build_messages.assert_called_once()
            service.add_messages.assert_called_once_with(messages=["a"])
            service.notify_all.assert_called_once()
