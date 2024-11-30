from datetime import datetime
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

from src.tasks.models import Task
from src.tasks.persistence import TaskDBPort
from src.tasks.settings import APP_NAME
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TASK = Task(tenant_id="tenant_123", title="Test Task")


class TestTaskAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.task_db: TaskDBPort = self.app.dependencies.persistence.get_repository(
            APP_NAME, "Task"
        )

    def test_get_task_no_login(self):
        response = self.client.get(
            f"{URL_API}/task/{USER_TASK.id}", headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    @patch("src.tasks.services.TasksService.get_user_task", return_value=USER_TASK)
    def test_get_task(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/task/{USER_TASK.id}", headers=headers)

        self.assertEqual(response.status_code, 200)

        mock_task.assert_called_once_with(user_id=self.user.id, task_id=USER_TASK.id)

    @patch("src.tasks.services.TasksService.update_task", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_task", return_value=USER_TASK)
    def test_update_task_put(self, mock_task: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        new_title = self.fake.sentence(nb_words=5)
        done_at = datetime.now(tz=ZoneInfo("UTC")).isoformat()
        data = {
            "title": new_title,
            "done": done_at,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/task/{USER_TASK.id}", json=data, headers=headers
            )

        done = datetime.fromisoformat(done_at)
        result_done = datetime.fromisoformat(response.json.get("done"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(USER_TASK.title, new_title)
        self.assertEqual(response.json.get("title"), new_title)
        self.assertEqual(result_done, done)
        self.assertFalse(response.json.get("emergency"))

        mock_task.assert_called_once_with(user_id=self.user.id, task_id=USER_TASK.id)
        mock_update.assert_called_once()

    @patch("src.tasks.services.TasksService.update_task", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_task", return_value=USER_TASK)
    def test_update_task_patch(self, mock_task: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        new_title = self.fake.sentence(nb_words=5)
        data = {
            "title": new_title,
            "emergency": True,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/task/{USER_TASK.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(USER_TASK.title, new_title)
        self.assertEqual(response.json.get("title"), new_title)
        self.assertTrue(response.json.get("emergency"))
        self.assertFalse(response.json.get("important"))

        mock_task.assert_called_once_with(user_id=self.user.id, task_id=USER_TASK.id)
        mock_update.assert_called_once()

    @patch("src.tasks.services.TasksService.delete_task", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_task", return_value=USER_TASK)
    def test_delete_task(self, mock_task: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/task/{USER_TASK.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_task.assert_called_once_with(user_id=self.user.id, task_id=USER_TASK.id)
        mock_delete.assert_called_once()
