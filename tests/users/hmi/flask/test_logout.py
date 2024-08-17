from unittest.mock import MagicMock, patch

from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API_USERS = "/api/v1/users"


class TestUserV1Logout(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/logout", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_get(self):
        response = self.client.get(f"{URL_API_USERS}/logout", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/logout", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/logout", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    @patch("src.users.hmi.flask.api.v1.logout.UsersService.logout", return_value=True)
    def test_post_logout(self, mock_logout: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API_USERS}/logout", headers=headers)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.text, "")

        mock_logout.assert_called_once_with(sha_token=self.token)

    @patch("src.users.hmi.flask.api.v1.logout.UsersService.logout", return_value=False)
    def test_post_logout_fake_token(self, mock_logout: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API_USERS}/logout", headers=headers)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, "application/json")

        mock_logout.assert_called_once_with(sha_token=self.token)
