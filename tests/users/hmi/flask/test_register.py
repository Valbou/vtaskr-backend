from unittest.mock import MagicMock, patch

from babel import Locale

from src.settings import LOCALE, TIMEZONE
from src.users.models import User
from tests.base_test import DummyBaseTestCase

URL_API_USERS = "/api/v1/users"

LOCAL_TEST_USER = User(
    first_name="First",
    last_name="Last",
    email="test@example.com",
    locale=Locale.parse(LOCALE),
    timezone=TIMEZONE,
)


class TestUserV1Register(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    @patch("src.users.services.UsersService.clean_unused_accounts")
    @patch(
        "src.users.services.UsersService.register",
        return_value=(LOCAL_TEST_USER, None),
    )
    def test_post_register(self, mock_register: MagicMock, mock_clean: MagicMock):
        user_data = {
            "first_name": LOCAL_TEST_USER.first_name,
            "last_name": LOCAL_TEST_USER.last_name,
            "email": LOCAL_TEST_USER.email,
            "password": self.generate_password(),
        }

        response = self.client.post(
            f"{URL_API_USERS}/register", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), user_data.get("first_name"))
        self.assertEqual(response.json.get("last_name"), user_data.get("last_name"))
        self.assertEqual(response.json.get("email"), user_data.get("email"))
        self.assertIsNone(response.json.get("hash_password"))

        mock_clean.assert_called_once()
        mock_register.assert_called_once()

    @patch("src.users.services.UsersService.clean_unused_accounts")
    def test_post_register_bad_email(self, mock_clean: MagicMock):
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": "valbou@fr",
            "password": self.generate_password(),
        }

        response = self.client.post(
            f"{URL_API_USERS}/register", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 400)

        mock_clean.assert_called_once()

    @patch("src.users.services.UsersService.clean_unused_accounts")
    def test_post_register_no_password(self, mock_clean: MagicMock):
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.generate_email(),
        }

        response = self.client.post(
            f"{URL_API_USERS}/register", json=user_data, headers=self.headers
        )

        self.assertEqual(response.status_code, 400)

        mock_clean.assert_not_called()

    def test_no_get(self):
        response = self.client.get(f"{URL_API_USERS}/register", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/register", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/register", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/register", headers=self.headers)
        self.assertEqual(response.status_code, 405)
