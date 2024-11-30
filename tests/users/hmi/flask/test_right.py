from unittest.mock import MagicMock, patch

from src.libs.iam.constants import Permissions
from src.users.models import Right, RoleType
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_RIGHT = Right(
    roletype_id="roletype_123",
    resource="RESOURCE",
    permissions=[Permissions.EXECUTE],
)
USER_ROLETYPE = RoleType(
    name="Test",
    group_id="group_123",
)


class TestRightAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def get_a_user_right(self) -> Right:
        return USER_RIGHT

    def test_get_right_no_login(self):
        self.create_user()

        response = self.client.get(
            f"{URL_API}/right/{USER_RIGHT.id}", headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    def test_get_my_right(self, mock_right: MagicMock, mock_roletype: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/right/{USER_RIGHT.id}", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock_right.assert_called_once_with(user_id=self.user.id, right_id=USER_RIGHT.id)
        mock_roletype.assert_called_once_with(
            user_id=self.user.id, roletype_id="roletype_123"
        )

    @patch(
        "src.users.services.UsersService.get_all_user_rights",
        return_value=[USER_RIGHT, USER_RIGHT],
    )
    def test_get_all_my_rights(self, mock_rights: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/rights", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 2)

        mock_rights.assert_called_once()

    @patch("src.users.services.UsersService.create_new_right", return_value=USER_RIGHT)
    def test_create_a_new_right(self, mock_right: MagicMock):
        headers = self.get_token_headers()

        data = {
            "resource": "Group",
            "permissions": sum([Permissions.READ, Permissions.EXECUTE]),
            "roletype_id": USER_ROLETYPE.id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API}/rights", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("roletype_id"), USER_RIGHT.roletype_id)

        mock_right.assert_called_once()

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    @patch("src.users.services.UsersService.update_user_right", return_value=True)
    def test_update_associated_right_put(
        self, mock_update: MagicMock, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        data = {
            "resource": USER_RIGHT.resource,
            "permissions": sum([Permissions.CREATE]),
            "roletype_id": USER_RIGHT.roletype_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/right/{USER_RIGHT.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("permissions"), 4)

        mock_right.assert_called_once()
        mock_roletype.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    @patch("src.users.services.UsersService.update_user_right", return_value=True)
    def test_update_associated_right_patch(
        self, mock_update: MagicMock, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        data = {
            "resource": USER_RIGHT.resource,
            "permissions": sum([Permissions.CREATE]),
            "roletype_id": USER_RIGHT.roletype_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/right/{USER_RIGHT.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("permissions"), 4)

        mock_right.assert_called_once()
        mock_roletype.assert_called_once()
        mock_update.assert_called_once()

    @patch("src.users.services.UsersService.get_user_roletype", return_value=None)
    @patch("src.users.services.UsersService.get_user_right", return_value=None)
    def test_update_stranger_right(
        self, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        data = {
            "resource": USER_RIGHT.resource,
            "permissions": sum([Permissions.CREATE]),
            "roletype_id": USER_RIGHT.roletype_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/right/{USER_RIGHT.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 404)

        mock_right.assert_called_once()
        mock_roletype.assert_not_called()

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    @patch("src.users.services.UsersService.update_user_right", return_value=False)
    def test_update_global_right(
        self, mock_update: MagicMock, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        data = {
            "resource": USER_RIGHT.resource,
            "permissions": sum([Permissions.READ]),
            "roletype_id": USER_RIGHT.roletype_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/right/{USER_RIGHT.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 403)

        mock_right.assert_called_once()
        mock_roletype.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    @patch("src.users.services.UsersService.delete_user_right", return_value=True)
    def test_delete_associated_right(
        self, mock_delete: MagicMock, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/right/{USER_RIGHT.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_right.assert_called_once()
        mock_roletype.assert_called_once()
        mock_delete.assert_called_once()

    @patch("src.users.services.UsersService.get_user_roletype", return_value=None)
    @patch("src.users.services.UsersService.get_user_right", return_value=None)
    def test_delete_stranger_right(
        self, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/right/{USER_RIGHT.id}", headers=headers
            )

        self.assertEqual(response.status_code, 404)

        mock_right.assert_called_once()
        mock_roletype.assert_not_called()

    @patch(
        "src.users.services.UsersService.get_user_roletype", return_value=USER_ROLETYPE
    )
    @patch("src.users.services.UsersService.get_user_right", return_value=USER_RIGHT)
    @patch("src.users.services.UsersService.delete_user_right", return_value=False)
    def test_delete_global_right(
        self, mock_delete: MagicMock, mock_right: MagicMock, mock_roletype: MagicMock
    ):
        headers = self.get_token_headers()

        right = self.get_a_user_right()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(f"{URL_API}/right/{right.id}", headers=headers)

        self.assertEqual(response.status_code, 403)

        mock_right.assert_called_once()
        mock_roletype.assert_called_once()
        mock_delete.assert_called_once()
