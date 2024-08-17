from unittest.mock import MagicMock, patch

from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"


class TestUserV1ChangeEmail(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.new_email = self.generate_email()
        self.headers = self.get_json_headers()

    @patch("src.users.hmi.flask.api.v1.change_email.UsersService.request_email_change")
    def test_change_email(self, mock: MagicMock):
        headers = self.get_token_headers()
        user_data = {"new_email": self.new_email}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/users/me/change-email", json=user_data, headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock.assert_called_once()

    @patch("src.users.hmi.flask.api.v1.change_email.UsersService.request_email_change")
    def test_change_invalid_email(self, mock: MagicMock):
        headers = self.get_token_headers()
        user_data = {"new_email": self.fake.word()}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/users/me/change-email", json=user_data, headers=headers
            )

        self.assertEqual(response.status_code, 400)

        mock.assert_not_called()

    def test_change_email_without_token(self):
        user_data = {"new_email": self.new_email}

        response = self.client.post(
            f"{URL_API}/users/me/change-email", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    def test_no_get(self):
        response = self.client.get(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)


class TestUserV1NewEmail(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.new_email = self.generate_email()

    @patch("src.users.hmi.flask.api.v1.change_email.UsersService.set_new_email")
    def test_set_new_email(self, mock: MagicMock):
        self.get_token_headers()

        user_data = {
            "old_email": self.user.email,
            "new_email": self.new_email,
            "hash": "hash_123",
            "code": "code_123",
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/new-email", json=user_data, headers=self.headers
            )

        self.assertEqual(response.status_code, 200)

        mock.assert_called_once_with(
            old_email=self.user.email,
            new_email=self.new_email,
            hash="hash_123",
            code="code_123",
        )

    def test_no_get(self):
        response = self.client.get(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)
