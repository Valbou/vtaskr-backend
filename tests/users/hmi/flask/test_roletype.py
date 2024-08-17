from unittest.mock import MagicMock, patch

from src.users.models import RoleType
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"


USER_ROLETYPE = RoleType(
    name="Test",
    group_id="group_123",
)


class TestRoleTypeAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_get_roletype_no_login(self):
        self.create_user()

        response = self.client.get(
            f"{URL_API}/roletype/{USER_ROLETYPE.id}", headers=self.headers
        )

        self.assertEqual(response.status_code, 401)

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.get_user_roletype",
        return_value=USER_ROLETYPE,
    )
    def test_get_my_roletype(self, mock_roletype: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/roletype/{USER_ROLETYPE.id}", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock_roletype.assert_called_once_with(
            user_id=self.user.id, roletype_id=USER_ROLETYPE.id
        )

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.get_all_user_roletypes",
        return_value=[USER_ROLETYPE, USER_ROLETYPE],
    )
    def test_get_all_my_roletypes(self, mock_roletypes: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/roletypes", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 2)

        mock_roletypes.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.create_new_roletype",
        return_value=[USER_ROLETYPE, True],
    )
    def test_create_a_new_roletype(self, mock_roletypes: MagicMock):
        headers = self.get_token_headers()

        name = self.fake.word()
        data = {
            "name": name,
            "group_id": self.group.id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(
                f"{URL_API}/roletypes", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("name"), USER_ROLETYPE.name)

        mock_roletypes.assert_called_once_with(name=name, group_id=self.group.id)

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.update_user_roletype",
        return_value=USER_ROLETYPE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.get_user_roletype",
        return_value=USER_ROLETYPE,
    )
    def test_update_roletype_put(
        self, mock_roletype: MagicMock, mock_update: MagicMock
    ):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {
            "name": new_name,
            "group_id": USER_ROLETYPE.group_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/roletype/{USER_ROLETYPE.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("name"), new_name)

        mock_roletype.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.update_user_roletype",
        return_value=USER_ROLETYPE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.get_user_roletype",
        return_value=USER_ROLETYPE,
    )
    def test_update_roletype_patch(
        self, mock_roletype: MagicMock, mock_update: MagicMock
    ):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {
            "name": new_name,
            "group_id": USER_ROLETYPE.group_id,
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/roletype/{USER_ROLETYPE.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("name"), new_name)

        mock_roletype.assert_called_once()
        mock_update.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.delete_user_roletype",
        return_value=USER_ROLETYPE,
    )
    @patch(
        "src.users.hmi.flask.api.v1.roletype.UsersService.get_user_roletype",
        return_value=USER_ROLETYPE,
    )
    def test_delete_roletype(self, mock_roletype: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/roletype/{USER_ROLETYPE.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_roletype.assert_called_once()
        mock_delete.assert_called_once()
