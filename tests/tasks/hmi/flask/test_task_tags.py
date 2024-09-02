from unittest.mock import MagicMock, patch

from src.tasks.models import Tag, Task
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TASK = Task(tenant_id="tenant_123", title="Test Task")
USER_TAG = Tag(tenant_id="tenant_123", title="Test Tag")


class TestTaskTagsAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def create_data(self, session):
        USER_TASK.add_tags([USER_TAG])

    @patch("src.tasks.services.TasksService.get_all_task_tags", return_value=[USER_TAG])
    @patch("src.tasks.services.TasksService.get_user_task", return_value=USER_TASK)
    def test_task_tags(self, mock_task: MagicMock, mock_tags: MagicMock):
        headers = self.get_token_headers()
        USER_TASK.add_tags([USER_TAG])

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/task/{USER_TASK.id}/tags", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        for tag in result:
            with self.subTest(tag.get("id")):
                self.assertIn(tag.get("id"), [USER_TAG.id])

        mock_task.assert_called_once()
        mock_tags.assert_called_once()

    @patch("src.tasks.services.TasksService.set_tags_to_task", return_value=False)
    def test_task_set_bad_tags(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        # Check with bad data
        data = {"tag_ids": ["123", "abc"]}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/task/{USER_TASK.id}/tags", json=data, headers=headers
            )
        self.assertEqual(response.status_code, 403)

        mock_task.assert_called_once()

    @patch("src.tasks.services.TasksService.set_tags_to_task", return_value=True)
    def test_task_set_tags(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        data = {"tag_ids": [USER_TAG.id]}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/task/{USER_TASK.id}/tags", json=data, headers=headers
            )
        self.assertEqual(response.status_code, 200)

        mock_task.assert_called_once()

    @patch("src.tasks.services.TasksService.set_tags_to_task", return_value=True)
    def test_task_remove_tags(self, mock_task: MagicMock):
        headers = self.get_token_headers()

        data = {"tag_ids": []}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/task/{USER_TASK.id}/tags", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)

        mock_task.assert_called_once()
