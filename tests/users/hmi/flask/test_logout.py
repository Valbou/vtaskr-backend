from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Logout(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_post(self):
        response = self.client.post(f"{URL_API_USERS}/logout", headers=self.headers)
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

    def test_delete_logout(self):
        headers = self.get_token_headers()
        payload = {"email": self.user.email}
        response = self.client.delete(
            f"{URL_API_USERS}/logout", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.text, "")

    def test_delete_logout_fake_token(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.fake.word()}",
        }
        response = self.client.delete(f"{URL_API_USERS}/logout", headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
