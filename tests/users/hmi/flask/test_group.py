from tests.base_test import BaseTestCase
from vtaskr.users.services import GroupService

URL_API = "/api/v1"


class TestGroupAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_get_group_no_login(self):
        self.create_user()
        response = self.client.get(
            f"{URL_API}/group/{self.group.id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 401)

    def test_get_group(self):
        headers = self.get_token_headers()
        response = self.client.get(f"{URL_API}/group/{self.group.id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_group_put(self):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {"name": new_name}
        response = self.client.put(
            f"{URL_API}/group/{self.group.id}", json=data, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.group.name, new_name)
        self.assertEqual(response.json.get("name"), new_name)

    def test_update_group_patch(self):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {"name": new_name}
        response = self.client.patch(
            f"{URL_API}/group/{self.group.id}", json=data, headers=headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.group.name, new_name)
        self.assertEqual(response.json.get("name"), new_name)

    def test_delete_private_group(self):
        headers = self.get_token_headers()
        response = self.client.delete(
            f"{URL_API}/group/{self.group.id}", headers=headers
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"{URL_API}/group/{self.group.id}", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_group(self):
        headers = self.get_token_headers()

        with self.app.sql.get_session() as session:
            self.group_service = GroupService(session=session)
            group = self.group_service.create_group(
                user=self.user, group_name=self.fake.word()
            )

            response = self.client.get(f"{URL_API}/group/{group.id}", headers=headers)
            self.assertEqual(response.status_code, 200)

            response = self.client.delete(
                f"{URL_API}/group/{group.id}", headers=headers
            )
            self.assertEqual(response.status_code, 204)

            response = self.client.get(f"{URL_API}/group/{group.id}", headers=headers)
            self.assertEqual(response.status_code, 404)
