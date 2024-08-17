from unittest.mock import MagicMock, patch

from tests.base_test import DummyBaseTestCase

URL_API = "/api/v1"


class TestUserV1ForgottenPassword(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    @patch(
        "src.users.hmi.flask.api.v1.change_password.UsersService.request_password_change"
    )
    @patch("src.users.hmi.flask.api.v1.change_password.UsersService.find_user_by_email")
    def test_forgotten_password(self, mock_1: MagicMock, mock_2: MagicMock):
        self.create_user()
        user_data = {"email": self.user.email}

        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        mock_1.assert_called_once_with(email=self.user.email)
        mock_2.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.change_password.UsersService.request_password_change"
    )
    @patch(
        "src.users.hmi.flask.api.v1.change_password.UsersService.find_user_by_email",
        return_value=None,
    )
    def test_forgotten_password_unknown_email(
        self, mock_1: MagicMock, mock_2: MagicMock
    ):
        self.create_user()
        user_data = {"email": self.generate_email()}

        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        mock_1.assert_called_once_with(email=user_data.get("email"))
        mock_2.assert_not_called()

    def test_no_get(self):
        response = self.client.get(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)


class TestUserV1NewPassword(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.new_password = self.generate_password()

    @patch("src.users.hmi.flask.api.v1.change_password.UsersService.set_new_password")
    def test_set_new_password(self, mock: MagicMock):
        email = "test@example.com"
        user_data = {
            "email": email,
            "hash": "hash_123",
            "new_password": self.new_password,
        }

        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        mock.assert_called_once_with(
            email=email, hash="hash_123", password=self.new_password
        )

    @patch(
        "src.users.hmi.flask.api.v1.change_password.UsersService.set_new_password",
        return_value=False,
    )
    def test_set_new_password_bad_hash(self, mock: MagicMock):
        email = "test@example.com"
        bad_hash = self.fake.word()
        user_data = {
            "email": email,
            "hash": bad_hash,
            "new_password": self.new_password,
        }

        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

        mock.assert_called_once_with(
            email=email, hash=bad_hash, password=self.new_password
        )

    @patch(
        "src.users.hmi.flask.api.v1.change_password.UsersService.set_new_password",
        return_value=False,
    )
    def test_set_new_password_bad_email(self, mock: MagicMock):
        email = self.generate_email()
        user_data = {
            "email": email,
            "hash": "hash_123",
            "new_password": self.new_password,
        }

        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

        mock.assert_called_once_with(
            email=email, hash="hash_123", password=self.new_password
        )

    def test_no_get(self):
        response = self.client.get(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)
