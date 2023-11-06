from src.users.models import RoleType
from src.users.services import RoleTypeService
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestRoleTypeAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def get_a_user_roletype(self, session) -> RoleType:
        roletype_service = RoleTypeService(session=session)
        roletypes = roletype_service.get_all_roletypes(self.user.id)
        return roletypes[0]

    def test_get_roletype_no_login(self):
        self.create_user()
        with self.app.sql.get_session() as session:
            roletype = self.get_a_user_roletype(session=session)

            response = self.client.get(
                f"{URL_API}/roletype/{roletype.id}", headers=self.headers
            )
            self.assertEqual(response.status_code, 401)

    def test_get_my_roletype(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            roletype = self.get_a_user_roletype(session=session)

            response = self.client.get(
                f"{URL_API}/roletype/{roletype.id}", headers=headers
            )
            self.assertEqual(response.status_code, 200)

    def test_get_all_my_roletypes(self):
        headers = self.get_token_headers()
        response = self.client.get(f"{URL_API}/roletypes", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        # Admin and Observer default global role types
        self.assertEqual(len(response.json), 2)

    def test_create_a_new_roletype(self):
        headers = self.get_token_headers()

        name = self.fake.word()
        data = {
            "name": name,
            "group_id": self.group.id,
        }
        response = self.client.post(f"{URL_API}/roletypes", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("name"), name)

    def test_update_roletype_put(self):
        headers = self.get_token_headers()

        with self.app.sql.get_session() as session:
            roletype_service = RoleTypeService(session=session)
            roletype = roletype_service.create_custom_roletype(
                self.fake.word(), self.group.id
            )

            new_name = self.fake.word()
            data = {
                "name": new_name,
                "group_id": roletype.group_id,
            }
            response = self.client.put(
                f"{URL_API}/roletype/{roletype.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json.get("name"), new_name)

    def test_update_stranger_roletype(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        with self.app.sql.get_session() as session:
            roletype_service = RoleTypeService(session=session)
            roletype = roletype_service.create_custom_roletype(
                self.fake.word(), self.group.id
            )

            new_name = self.fake.word()
            data = {
                "name": new_name,
                "group_id": self.group_0.id,
            }
            response = self.client.patch(
                f"{URL_API}/roletype/{roletype.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 404)

    def test_update_global_roletype(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            roletype = self.get_a_user_roletype(session=session)

            new_name = self.fake.word()
            data = {
                "name": new_name,
                "group_id": self.group.id,
            }
            response = self.client.put(
                f"{URL_API}/roletype/{roletype.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_associated_roletype(self):
        headers = self.get_token_headers()

        with self.app.sql.get_session() as session:
            roletype_service = RoleTypeService(session=session)
            roletype = roletype_service.create_custom_roletype(
                self.fake.word(), self.group.id
            )

            response = self.client.delete(
                f"{URL_API}/roletype/{roletype.id}", headers=headers
            )
            self.assertEqual(response.status_code, 204)

    def test_delete_stranger_roletype(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        with self.app.sql.get_session() as session:
            roletype_service = RoleTypeService(session=session)
            roletype = roletype_service.create_custom_roletype(
                self.fake.word(), self.group.id
            )

            response = self.client.delete(
                f"{URL_API}/roletype/{roletype.id}", headers=headers
            )
            self.assertEqual(response.status_code, 404)

    def test_delete_global_roletype(self):
        headers = self.get_token_headers()

        with self.app.sql.get_session() as session:
            roletype = self.get_a_user_roletype(session=session)

            response = self.client.delete(
                f"{URL_API}/roletype/{roletype.id}", headers=headers
            )
            self.assertEqual(response.status_code, 403)
