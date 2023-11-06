from src.users.models import Role
from src.users.services import RoleService, RoleTypeService
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestRoleAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def get_a_test_user_role(self, session) -> Role:
        self.role_service = RoleService(session=session)
        roles = self.role_service.get_all_roles(self.user.id)
        return roles[0]

    def get_a_colleague_role(self, session) -> Role:
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        role_service = RoleService(session=session)
        roletype_service = RoleTypeService(session=session)
        roletype = roletype_service.get_default_admin()

        role = Role(self.user.id, self.group_0.id, roletype_id=roletype.id)
        return role_service.create_role(
            user_id=self.user_0.id,
            role=role,
        )

    def test_get_role_no_login(self):
        self.create_user()
        with self.app.sql.get_session() as session:
            role = self.get_a_test_user_role(session=session)

            response = self.client.get(
                f"{URL_API}/role/{role.id}", headers=self.headers
            )
            self.assertEqual(response.status_code, 401)

    def test_get_my_role(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_test_user_role(session=session)

            response = self.client.get(f"{URL_API}/role/{role.id}", headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_get_all_my_roles(self):
        headers = self.get_token_headers()
        response = self.client.get(f"{URL_API}/roles", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_create_a_new_role(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        with self.app.sql.get_session() as session:
            roletype_service = RoleTypeService(session=session)
            roletype = roletype_service.get_default_admin()

            data = {
                "user_id": self.user.id,
                "group_id": self.group_0.id,
                "roletype_id": roletype.id,
            }
            response = self.client.post(f"{URL_API}/roles", json=data, headers=headers)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json.get("roletype_id"), roletype.id)

    def test_get_colleague_role(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_colleague_role(session=session)

            response = self.client.get(f"{URL_API}/role/{role.id}", headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_update_colleague_role_put(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_colleague_role(session=session)

            # Downgrade to Observer role
            self.roletype_service = RoleTypeService(session=session)
            roletype = self.roletype_service.get_default_observer()

            data = {
                "group_id": role.group_id,
                "user_id": role.user_id,
                "roletype_id": roletype.id,
            }
            response = self.client.put(
                f"{URL_API}/role/{role.id}", json=data, headers=headers
            )

            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(role.roletype_id, roletype.id)
            self.assertEqual(response.json.get("roletype_id"), roletype.id)

    def test_update_my_role_put(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_test_user_role(session=session)

            # Downgrade to Observer role
            self.roletype_service = RoleTypeService(session=session)
            roletype = self.roletype_service.get_default_observer()

            data = {
                "group_id": role.group_id,
                "user_id": role.user_id,
                "roletype_id": roletype.id,
            }
            response = self.client.put(
                f"{URL_API}/role/{role.id}", json=data, headers=headers
            )

            self.assertEqual(response.status_code, 403)

    def test_update_colleague_role_patch(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_colleague_role(session=session)

            # Downgrade to Observer role
            self.roletype_service = RoleTypeService(session=session)
            roletype = self.roletype_service.get_default_observer()

            data = {
                "group_id": role.group_id,
                "user_id": role.user_id,
                "roletype_id": roletype.id,
            }
            response = self.client.patch(
                f"{URL_API}/role/{role.id}", json=data, headers=headers
            )

            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(role.roletype_id, roletype.id)
            self.assertEqual(response.json.get("roletype_id"), roletype.id)

    def test_delete_colleague_role(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_colleague_role(session=session)

            response = self.client.delete(f"{URL_API}/role/{role.id}", headers=headers)
            self.assertEqual(response.status_code, 204)

            response = self.client.get(f"{URL_API}/role/{role.id}", headers=headers)
            self.assertEqual(response.status_code, 404)

    def test_delete_my_role(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            role = self.get_a_test_user_role(session=session)

            response = self.client.delete(f"{URL_API}/role/{role.id}", headers=headers)
            self.assertEqual(response.status_code, 403)
