from unittest.mock import MagicMock, patch

from src.tasks.models import Task
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TASK = Task(tenant_id="tenant_123", title="Test Task")


class TestTasksAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_create_task_no_login(self):
        task_data = {
            "title": "test",
            "tenant_id": "tenant_123",
        }

        response = self.client.post(
            f"{URL_API}/tasks", json=task_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    @patch("src.tasks.services.TasksService.create_new_task", return_value=True)
    def test_create_task(self, mock_create: MagicMock):
        headers = self.get_token_headers()
        task_data = {
            "title": USER_TASK.title,
            "tenant_id": USER_TASK.tenant_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/tasks", json=task_data, headers=headers
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("title"), USER_TASK.title)
        self.assertIsInstance(response.json.get("id"), str)

        mock_create.assert_called_once()

    def test_get_tasks_no_login(self):
        response = self.client.get(f"{URL_API}/tasks", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    @patch(
        "src.tasks.services.TasksService.get_user_all_tasks", return_value=[USER_TASK]
    )
    def test_get_tasks(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/tasks", headers=headers)

        self.assertEqual(response.status_code, 200)
        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get("id"), USER_TASK.id)

        mock_task.assert_called_once()

    @patch("src.tasks.services.TasksService.get_user_all_tasks", return_value=[])
    def test_get_tasks_with_filter(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/tasks?title_ncontains={USER_TASK.title}", headers=headers
            )

        self.assertEqual(response.status_code, 200)
        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        mock_task.assert_called_once()

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/tasks", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/tasks", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/tasks", headers=self.headers)
        self.assertEqual(response.status_code, 405)
