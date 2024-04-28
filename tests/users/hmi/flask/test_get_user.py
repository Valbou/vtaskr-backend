from zoneinfo import ZoneInfo

from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Me(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_post(self):
        response = self.client.post(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_get_me(self):
        headers = self.get_token_headers()
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
