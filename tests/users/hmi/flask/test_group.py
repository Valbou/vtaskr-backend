from unittest.mock import MagicMock, patch

from src.users.models import Group
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"


class TestGroupAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Test Group", is_private=False),
    )
    def test_get_group_no_login(self, mock_group: MagicMock):
        self.create_user()

        response = self.client.get(
            f"{URL_API}/group/{self.group.id}", headers=self.headers
        )

        mock_group.assert_not_called()

        self.assertEqual(response.status_code, 401)

    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Test Group", is_private=False),
    )
    def test_get_group(self, mock: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/group/{self.group.id}", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock.assert_called_once_with(user_id=self.user.id, group_id=self.group.id)

    @patch(
        "src.users.services.UsersService.create_new_group",
        return_value=Group(name="Test Group", is_private=False),
    )
    def test_create_group(self, mock: MagicMock):
        headers = self.get_token_headers()

        name = "Test Group"
        data = {"name": name}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API}/groups", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("name"), name)

        mock.assert_called_with(user_id=self.user.id, group_name=name, is_private=False)

    @patch(
        "src.users.services.UsersService.get_all_user_groups",
        return_value=[Group(name="Test Group", is_private=False)],
    )
    def test_get_all_groups(self, mock: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(f"{URL_API}/groups", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

        mock.assert_called_once()

    @patch("src.users.services.UsersService.update_group", return_value=True)
    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Private", is_private=True),
    )
    def test_update_group_put(self, mock_get: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {"name": new_name}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.put(
                f"{URL_API}/group/{self.group.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.group.name, new_name)
        self.assertEqual(response.json.get("name"), new_name)

        mock_get.assert_called_once_with(user_id=self.user.id, group_id=self.group.id)
        mock_update.assert_called_once()

    @patch("src.users.services.UsersService.update_group", return_value=True)
    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Private", is_private=True),
    )
    def test_update_group_patch(self, mock_get: MagicMock, mock_update: MagicMock):
        headers = self.get_token_headers()

        new_name = self.fake.word()
        data = {"name": new_name}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.patch(
                f"{URL_API}/group/{self.group.id}", json=data, headers=headers
            )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.group.name, new_name)
        self.assertEqual(response.json.get("name"), new_name)

        mock_get.assert_called_once_with(user_id=self.user.id, group_id=self.group.id)
        mock_update.assert_called_once()

    @patch("src.users.services.UsersService.delete_group", return_value=True)
    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Private", is_private=True),
    )
    def test_delete_private_group(self, mock_get: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/group/{self.group.id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_get.assert_called_once()
        mock_delete.assert_called_once()

    @patch("src.users.services.UsersService.delete_group", return_value=True)
    @patch(
        "src.users.services.UsersService.get_group",
        return_value=Group(name="Test Group", is_private=False),
    )
    def test_delete_group(self, mock_get: MagicMock, mock_delete: MagicMock):
        headers = self.get_token_headers()

        group_id = "group_123"

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.delete(
                f"{URL_API}/group/{group_id}", headers=headers
            )

        self.assertEqual(response.status_code, 204)

        mock_get.assert_called_once()
        mock_delete.assert_called_once()
