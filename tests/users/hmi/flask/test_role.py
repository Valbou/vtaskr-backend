from unittest.mock import MagicMock, patch

from src.users.models import Role
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_ROLE = Role(user_id="user_123", group_id="group_123", roletype_id="roletype_123")


class TestRoleAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_get_role_no_login(self):
        self.create_user()

        response = self.client.get(
            f"{URL_API}/role/{USER_ROLE.id}", headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_user_role",
        return_value=USER_ROLE,
    )
    def test_get_my_role(self, mock_role: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/role/{USER_ROLE.id}", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock_role.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_all_user_roles",
        return_value=[USER_ROLE, USER_ROLE],
    )
    def test_get_all_my_roles(self, mock_roles: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/roles", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 2)

        mock_roles.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.create_new_role",
        return_value=USER_ROLE,
    )
    def test_create_a_new_role(self, mock_role: MagicMock):
        headers = self.get_token_headers()

        data = {
            "user_id": "user_123",
            "group_id": "group_123",
            "roletype_id": "roletype_123",
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API}/roles", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("roletype_id"), "roletype_123")

        mock_role.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_user_role",
        return_value=USER_ROLE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.update_user_role",
        return_value=True,
    )
    def test_update_role_put(self, mock_update: MagicMock, mock_role: MagicMock):
        headers = self.get_token_headers()

        data = {
            "user_id": "user_123",
            "group_id": "group_123",
            "roletype_id": "roletype_123",
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/role/{USER_ROLE.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("roletype_id"), "roletype_123")

        mock_role.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_user_role",
        return_value=USER_ROLE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.update_user_role",
        return_value=True,
    )
    def test_update_role_patch(self, mock_update: MagicMock, mock_role: MagicMock):
        headers = self.get_token_headers()

        data = {
            "user_id": "user_123",
            "group_id": "group_123",
            "roletype_id": "roletype_123",
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/role/{USER_ROLE.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("roletype_id"), "roletype_123")

        mock_role.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_user_role",
        return_value=USER_ROLE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.delete_user_role",
        return_value=True,
    )
    def test_delete_role(self, mock_delete: MagicMock, mock_role: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/role/{USER_ROLE.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_role.assert_called_once()
        mock_delete.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.get_user_role",
        return_value=USER_ROLE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.role.UsersService.delete_user_role",
        return_value=False,
    )
    def test_delete_my_role(self, mock_delete: MagicMock, mock_role: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/role/{USER_ROLE.id}", headers=headers
            )

        self.assertEqual(response.status_code, 403)

        mock_role.assert_called_once()
        mock_delete.assert_called_once()
