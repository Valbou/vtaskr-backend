from unittest.mock import MagicMock, patch

from src.tasks.models import Tag
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TAG = Tag(tenant_id="tenant_123", title="Test Tag")


class TestTagsAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_create_tag_no_login(self):
        tag_data = {
            "title": USER_TAG.title,
            "tenant_id": USER_TAG.tenant_id,
        }

        response = self.client.post(
            f"{URL_API}/tags", json=tag_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    def test_get_tags_no_login(self):
        response = self.client.get(f"{URL_API}/tags", headers=self.headers)

        self.assertEqual(response.status_code, 401)

    @patch("src.tasks.services.TasksService.create_new_tag", return_value=True)
    def test_create_tag(self, mock_create: MagicMock):
        headers = self.get_token_headers()

        tag_data = {
            "title": USER_TAG.title,
            "tenant_id": USER_TAG.tenant_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/tags", json=tag_data, headers=headers
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("title"), USER_TAG.title)
        self.assertIsInstance(response.json.get("id"), str)

        mock_create.assert_called_once()

    @patch("src.tasks.services.TasksService.get_user_all_tags", return_value=[USER_TAG])
    def test_get_tags(self, mock_tags: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/tags", headers=headers)

        self.assertEqual(response.status_code, 200)
        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get("title"), USER_TAG.title)

        mock_tags.assert_called_once()

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)
