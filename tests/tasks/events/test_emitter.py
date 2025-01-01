from unittest import TestCase
from unittest.mock import MagicMock

from src.tasks.events import TasksEventManager


class TestTasksEventManager(TestCase):
    def setUp(self):
        super().setUp()

        self.manager = TasksEventManager()

    def test_send_tasks_todo_today_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_tasks_todo_today_event(
            session=mock_session,
            assigned_to="assigned_123",
            today_tasks=[],
            tomorrow_tasks=[],
        )

        mock_session.emit.assert_called_once()
