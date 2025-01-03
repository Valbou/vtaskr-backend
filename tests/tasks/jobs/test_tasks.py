from unittest.mock import MagicMock, patch

from src.tasks.jobs.tasks import run_dailys_tasks
from tests.base_test import DummyCeleryTestCase


class TestTasksTasks(DummyCeleryTestCase):
    def test_run_dailys_tasks(self):
        with patch("src.tasks.jobs.tasks.TasksService") as MockClass:
            service = MockClass.return_value
            service.send_today_tasks_notifications = MagicMock()

            run_dailys_tasks()

            service.send_today_tasks_notifications.assert_called_once()