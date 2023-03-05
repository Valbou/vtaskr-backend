from tests import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Update(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_post(self):
        response = self.client.post(f"{URL_API_USERS}/me/update", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_get(self):
        response = self.client.get(f"{URL_API_USERS}/me/update", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_put_user(self):
        new_first_name = self.fake.first_name()
        headers = self.get_token_headers()
        payload = {"first_name": new_first_name}
        response = self.client.put(
            f"{URL_API_USERS}/me/update", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), new_first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)
        self.assertIsNone(response.json.get("hash_password"))

    def test_patch_user(self):
        new_last_name = self.fake.last_name()
        headers = self.get_token_headers()
        payload = {"last_name": new_last_name}
        response = self.client.patch(
            f"{URL_API_USERS}/me/update", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), new_last_name)
        self.assertIsNone(response.json.get("hash_password"))

    def test_no_delete(self):
        response = self.client.delete(
            f"{URL_API_USERS}/me/update", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)
