from src.libs.iam.constants import Permissions
from src.users.models import Right
from src.users.services import RightService, RoleTypeService
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestRightAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def get_a_user_right(self) -> Right:
        right_service = RightService(self.app.dependencies)
        rights = right_service.get_all_rights(self.user.id)
        return rights[0]

    def test_get_right_no_login(self):
        self.create_user()
        right = self.get_a_user_right()

        response = self.client.get(f"{URL_API}/right/{right.id}", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_get_my_right(self):
        headers = self.get_token_headers()
        right = self.get_a_user_right()

        response = self.client.get(f"{URL_API}/right/{right.id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_my_rights(self):
        headers = self.get_token_headers()
        response = self.client.get(f"{URL_API}/rights", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(
            len(response.json), len(self.app.dependencies.identity.get_resources())
        )

    def test_create_a_new_right(self):
        headers = self.get_token_headers()

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            self.fake.word(), self.group.id
        )

        data = {
            "resource": "Group",
            "permissions": sum([Permissions.READ, Permissions.EXECUTE]),
            "roletype_id": roletype.id,
        }
        response = self.client.post(f"{URL_API}/rights", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("roletype_id"), roletype.id)

    def test_update_associated_right_put(self):
        headers = self.get_token_headers()

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            self.fake.word(), self.group.id
        )

        right_service = RightService(self.app.dependencies)
        right = Right(
            roletype_id=roletype.id,
            resource="RoleType",
            permissions=[Permissions.READ, Permissions.EXECUTE],
        )
        right = right_service.create_right(self.user.id, self.group.id, right)

        data = {
            "resource": right.resource,
            "permissions": sum([Permissions.CREATE]),
            "roletype_id": right.roletype_id,
        }
        response = self.client.put(
            f"{URL_API}/right/{right.id}", json=data, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("permissions"), 4)

    def test_update_stranger_right(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            self.fake.word(), self.group.id
        )

        right_service = RightService(self.app.dependencies)
        right = Right(
            roletype_id=roletype.id,
            resource="RoleType",
            permissions=[Permissions.READ, Permissions.EXECUTE],
        )
        right = right_service.create_right(self.user.id, self.group.id, right)

        data = {
            "resource": right.resource,
            "permissions": sum([Permissions.CREATE]),
            "roletype_id": right.roletype_id,
        }
        response = self.client.patch(
            f"{URL_API}/right/{right.id}", json=data, headers=headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_global_right(self):
        headers = self.get_token_headers()

        right = self.get_a_user_right()

        data = {
            "resource": right.resource,
            "permissions": sum([Permissions.READ]),
            "roletype_id": right.roletype_id,
        }
        response = self.client.put(
            f"{URL_API}/right/{right.id}", json=data, headers=headers
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_associated_right(self):
        headers = self.get_token_headers()

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            self.fake.word(), self.group.id
        )

        right_service = RightService(self.app.dependencies)
        right = Right(
            roletype_id=roletype.id,
            resource="RoleType",
            permissions=[Permissions.READ, Permissions.EXECUTE],
        )
        right = right_service.create_right(self.user.id, self.group.id, right)

        response = self.client.delete(f"{URL_API}/right/{right.id}", headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_delete_stranger_right(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            self.fake.word(), self.group.id
        )

        right_service = RightService(self.app.dependencies)
        right = Right(
            roletype_id=roletype.id,
            resource="RoleType",
            permissions=[Permissions.READ, Permissions.EXECUTE],
        )
        right = right_service.create_right(self.user.id, self.group.id, right)

        response = self.client.delete(f"{URL_API}/right/{right.id}", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_global_right(self):
        headers = self.get_token_headers()

        right = self.get_a_user_right()

        response = self.client.delete(f"{URL_API}/right/{right.id}", headers=headers)
        self.assertEqual(response.status_code, 403)
