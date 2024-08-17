from unittest.mock import ANY, MagicMock, patch

from src.users.models import Invitation, Role
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"


class TestInvitationAPI(DummyBaseTestCase):
    @patch(
        "src.users.hmi.flask.api.v1.invitation.UsersService.invite_user_by_email",
        return_value=Invitation(
            from_user_id="user_123",
            to_user_email="test@example.com",
            with_roletype_id="roletype_123",
            in_group_id="group_123",
        ),
    )
    def test_invite_a_new_user(self, mock: MagicMock):
        headers = self.get_token_headers()

        data = {
            "to_user_email": "test@example.com",
            "with_roletype_id": "roletype_123",
            "in_group_id": "group_123",
        }

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.post(f"{URL_API}/invite", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        mock.assert_called_once_with(
            user=ANY,
            user_email="test@example.com",
            group_id="group_123",
            roletype_id="roletype_123",
        )

    @patch(
        "src.users.hmi.flask.api.v1.invitation.UsersService.accept_invitation",
        return_value=Role(
            user_id="user_123",
            roletype_id="roletype_123",
            group_id="group_123",
        ),
    )
    def test_accept_invitation(self, mock: MagicMock):
        headers_accept = self.get_token_headers()
        data_accept = {"hash": "hash_123"}

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response_accept = self.client.post(
                f"{URL_API}/invite/accepted", json=data_accept, headers=headers_accept
            )

        self.assertEqual(response_accept.status_code, 200)

        mock.assert_called_once()

    @patch(
        "src.users.hmi.flask.api.v1.invitation.UsersService.get_invitations",
        return_value=[
            Invitation(
                from_user_id="user_123",
                to_user_email="test@example.com",
                with_roletype_id="roletype_123",
                in_group_id="group_123",
            )
        ],
    )
    def test_get_invitations(self, mock: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/group/{self.group.id}/invitations", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock.assert_called_once_with(user_id=self.user.id, group_id=self.group.id)

    @patch("src.users.hmi.flask.api.v1.invitation.UsersService.delete_invitation")
    def test_cancel_invitation(self, mock: MagicMock):
        headers = self.get_token_headers()
        invitation_id = "invitation_123"

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response_accept = self.client.delete(
                f"{URL_API}/invite/{invitation_id}", headers=headers
            )

        self.assertEqual(response_accept.status_code, 204)

        mock.assert_called_once_with(user=ANY, invitation_id="invitation_123")
