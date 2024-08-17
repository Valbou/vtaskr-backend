from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API_USERS = "/api/v1/users"


class TestUserV1Me(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_post(self):
        response = self.client.post(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_get_me(self):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API_USERS}/me", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("id"), self.user.id)
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)
        self.assertEqual(response.json.get("email"), self.user.email)
        self.assertEqual(
            response.json.get("created_at"),
            self.user.created_at.astimezone(ZoneInfo("UTC")).isoformat(),
        )

    @patch("src.users.services.UsersService.update_user")
    def test_put_user(self, mock_user: MagicMock):
        headers = self.get_token_headers()

        new_first_name = self.fake.first_name()
        payload = {
            "first_name": new_first_name,
            "last_name": self.user.last_name,
            "locale": str(self.user.locale),
            "timezone": self.user.timezone,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API_USERS}/me", headers=headers, json=payload
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), new_first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)
        self.assertEqual(response.json.get("locale"), str(self.user.locale))
        self.assertEqual(response.json.get("timezone"), self.user.timezone)
        self.assertIsNone(response.json.get("hash_password"))

        mock_user.assert_called_once()

    @patch("src.users.services.UsersService.update_user")
    def test_patch_user(self, mock_user: MagicMock):
        headers = self.get_token_headers()

        new_last_name = self.fake.last_name()
        payload = {
            "first_name": self.user.first_name,
            "last_name": new_last_name,
            "locale": str(self.user.locale),
            "timezone": self.user.timezone,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API_USERS}/me", headers=headers, json=payload
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), new_last_name)
        self.assertEqual(response.json.get("locale"), str(self.user.locale))
        self.assertEqual(response.json.get("timezone"), self.user.timezone)
        self.assertIsNone(response.json.get("hash_password"))

        mock_user.assert_called_once()

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    @patch("src.users.services.UsersService.delete_user")
    def test_delete(self, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(f"{URL_API_USERS}/me", headers=headers)

        self.assertEqual(response.status_code, 204)

        mock_delete.assert_called_once()
