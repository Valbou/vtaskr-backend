from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Register(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_post_register(self):
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.generate_email(),
            "password": self.fake.password(),
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

    def test_post_register_bad_email(self):
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": "valbou@fr",
            "password": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/register", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_post_register_no_password(self):
        user_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.generate_email(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/register", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

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
