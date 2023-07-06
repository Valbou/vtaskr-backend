from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Confirm2FA(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_post_confirm_2FA(self):
        headers = self.get_token_headers(valid=False)
        payload = {
            "code_2FA": self.token.temp_code,
        }
        response = self.client.post(
            f"{URL_API_USERS}/2fa", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_post_bad_code_2FA(self):
        headers = self.get_token_headers(valid=False)
        payload = {
            "code_2FA": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/2fa", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")

    def test_no_get(self):
        response = self.client.get(f"{URL_API_USERS}/2fa", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/2fa", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/2fa", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/2fa", headers=self.headers)
        self.assertEqual(response.status_code, 405)
