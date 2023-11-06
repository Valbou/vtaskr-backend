from src.users.services import GroupService
from tests.base_test import BaseTestCase

URL_API_USERS = "/api/v1/users"


class TestUserV1Update(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_no_post(self):
        response = self.client.post(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_put_user(self):
        new_first_name = self.fake.first_name()
        headers = self.get_token_headers()
        payload = {
            "first_name": new_first_name,
            "last_name": self.user.last_name,
            "locale": str(self.user.locale),
            "timezone": self.user.timezone,
        }
        response = self.client.put(f"{URL_API_USERS}/me", headers=headers, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), new_first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)
        self.assertEqual(response.json.get("locale"), str(self.user.locale))
        self.assertEqual(response.json.get("timezone"), self.user.timezone)
        self.assertIsNone(response.json.get("hash_password"))

    def test_patch_user(self):
        new_last_name = self.fake.last_name()
        headers = self.get_token_headers()
        payload = {
            "first_name": self.user.first_name,
            "last_name": new_last_name,
            "locale": str(self.user.locale),
            "timezone": self.user.timezone,
        }
        response = self.client.patch(
            f"{URL_API_USERS}/me", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), new_last_name)
        self.assertEqual(response.json.get("locale"), str(self.user.locale))
        self.assertEqual(response.json.get("timezone"), self.user.timezone)
        self.assertIsNone(response.json.get("hash_password"))

    def test_no_put(self):
        response = self.client.put(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API_USERS}/me", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_delete(self):
        headers = self.get_token_headers()
        response = self.client.delete(f"{URL_API_USERS}/me", headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_no_delete_with_2_admin_groups(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            group_service = GroupService(session=session)
            group_service.create_group(self.user.id, "Another Group")

        response = self.client.delete(f"{URL_API_USERS}/me", headers=headers)
        self.assertEqual(response.status_code, 403)
