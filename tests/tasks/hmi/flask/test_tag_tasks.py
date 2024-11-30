from unittest.mock import MagicMock, patch

from src.tasks.models import Tag, Task
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TASK = Task(tenant_id="tenant_123", title="Test Task")
USER_TAG = Tag(tenant_id="tenant_123", title="Test Tag")


class TestTagTasksAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    @patch("src.tasks.services.TasksService.get_all_tag_tasks", return_value=[USER_TASK])
    @patch("src.tasks.services.TasksService.check_user_tag_exists", return_value=True)
    def test_tag_tasks(self, mock_tag: MagicMock, mock_tasks: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/tag/{USER_TAG.id}/tasks", headers=headers
            )
            self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        for task in result:
            with self.subTest(task.get("id")):
                self.assertIn(task.get("id"), [USER_TASK.id])

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_tasks.assert_called_once()

    @patch("src.tasks.services.TasksService.get_all_tag_tasks", return_value=[])
    @patch("src.tasks.services.TasksService.check_user_tag_exists", return_value=True)
    def test_tag_tasks_with_filter(self, mock_tag: MagicMock, mock_tasks: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/tag/{USER_TAG.id}/tasks?limit=1", headers=headers
            )
            self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_tasks.assert_called_once()
