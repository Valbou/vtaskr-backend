from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Login(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.headers = self.get_json_headers()

    def test_post_login(self):
        payload = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=self.headers, json=payload
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        token = response.json.get("token")
        self.assertEqual(len(token), 64)

    def test_post_login_unknown_user(self):
        payload = {
            "email": self.fake.email(domain="valbou.fr"),
            "password": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=self.headers, json=payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.text, '{"error": "Invalid credentials", "status": 401}'
        )

    def test_post_login_known_user_bad_password(self):
        payload = {
            "email": self.user.email,
            "password": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=self.headers, json=payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.text, '{"error": "Invalid credentials", "status": 401}'
        )

    def test_no_get(self):
        response = self.client.get(f"{URL_API_USERS}/login", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/login", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/login", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/login", headers=self.headers)
        self.assertEqual(response.status_code, 405)
