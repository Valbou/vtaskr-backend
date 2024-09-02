from unittest.mock import MagicMock, patch

from src.tasks.models import Tag
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_TAG = Tag(tenant_id="tenant_123", title="Test Tag")


class TestTagAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_get_tag_no_login(self):
        response = self.client.get(f"{URL_API}/tag/{USER_TAG.id}", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    @patch("src.tasks.services.TasksService.get_user_tag", return_value=USER_TAG)
    def test_get_tag(self, mock_tag: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/tag/{USER_TAG.id}", headers=headers)

        self.assertEqual(response.status_code, 200)

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)

    @patch("src.tasks.services.TasksService.get_user_tag", return_value=None)
    def test_get_tag_not_exists(self, mock_tag: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/tag/{USER_TAG.id}", headers=headers)

        self.assertEqual(response.status_code, 404)

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)

    @patch("src.tasks.services.TasksService.update_tag", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_tag", return_value=USER_TAG)
    def test_update_tag_put(self, mock_tag: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        background = self.fake.color()
        data = {
            "title": USER_TAG.title,
            "backgound_color": background,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/tag/{USER_TAG.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("title"), USER_TAG.title)
        result_background = response.json.get("backgound_color")
        self.assertEqual(result_background, background)
        result_foreground = response.json.get("text_color")
        self.assertEqual(result_foreground, "#FFFFFF")

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_update.assert_called_once()

    @patch("src.tasks.services.TasksService.update_tag", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_tag", return_value=USER_TAG)
    def test_update_tag_patch(self, mock_tag: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        background = self.fake.color()
        data = {
            "title": USER_TAG.title,
            "backgound_color": background,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/tag/{USER_TAG.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("title"), USER_TAG.title)
        result_background = response.json.get("backgound_color")
        self.assertEqual(result_background, background)
        result_foreground = response.json.get("text_color")
        self.assertEqual(result_foreground, "#FFFFFF")

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_update.assert_called_once()

    @patch("src.tasks.services.TasksService.delete_tag", return_value=True)
    @patch("src.tasks.services.TasksService.get_user_tag", return_value=USER_TAG)
    def test_delete_tag(self, mock_tag: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/tag/{USER_TAG.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_delete.assert_called_once()

    @patch("src.tasks.services.TasksService.delete_tag", return_value=False)
    @patch("src.tasks.services.TasksService.get_user_tag", return_value=USER_TAG)
    def test_no_delete_tag(self, mock_tag: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/tag/{USER_TAG.id}", headers=headers
            )

        self.assertEqual(response.status_code, 403)

        mock_tag.assert_called_once_with(user_id=self.user.id, tag_id=USER_TAG.id)
        mock_delete.assert_called_once()
