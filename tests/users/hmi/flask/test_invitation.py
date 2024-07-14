from src.users.services import UserService, RoleTypeService
from src.users.models import RoleType, Group, User

from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestInvitationAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_service = UserService(self.app.dependencies)
        self.roletype_service = RoleTypeService(self.app.dependencies)

    def create_group(self, user: User) -> Group:
        self.shared_group = self.user_service.create_group(
            user_id=user.id, group_name="My Shared Group"
        )

    def get_a_user_roletype(self, user: User) -> RoleType:
        roletypes = self.roletype_service.get_all_roletypes(user.id)
        return roletypes[0]

    def test_invite_a_new_user(self):
        headers = self.get_token_headers()
        self.user_0, self.group_0 = self.user, self.group
        self.create_user()

        self.create_group(user=self.user_0)
        roletype = self.get_a_user_roletype(user=self.user_0)

        invitations = self.user_service.get_invitations(
            user_id=self.user_0.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 0)

        data = {
            "to_user_email": self.user.email,
            "in_group_id": self.shared_group.id,
            "with_roletype_id": roletype.id,
        }

        response = self.client.post(f"{URL_API}/invite", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

        invitations = self.user_service.get_invitations(
            user_id=self.user_0.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 1)
        invitation = invitations[0]

        # Accept invitation
        headers_accept = self.get_token_headers()
        data_accept = {
            "hash": invitation.hash
        }

        response_accept = self.client.post(f"{URL_API}/invite/accepted", json=data_accept, headers=headers_accept)
        self.assertEqual(response_accept.status_code, 200)

        invitations = self.user_service.get_invitations(
            user_id=self.user_0.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 0)

    def test_invite_and_cancel(self):
        headers = self.get_token_headers()

        self.create_group(user=self.user)
        roletype = self.get_a_user_roletype(user=self.user)

        invitations = self.user_service.get_invitations(
            user_id=self.user.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 0)

        data = {
            "to_user_email": self.fake.email(domain="valbou.fr"),
            "in_group_id": self.shared_group.id,
            "with_roletype_id": roletype.id,
        }

        response = self.client.post(f"{URL_API}/invite", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

        invitations = self.user_service.get_invitations(
            user_id=self.user.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 1)
        invitation = invitations[0]

        # Cancel invitation
        response_accept = self.client.delete(f"{URL_API}/invite/{invitation.id}", headers=headers)
        print(response.status_code)
        self.assertEqual(response_accept.status_code, 204)

        invitations = self.user_service.get_invitations(
            user_id=self.user.id, group_id=self.shared_group.id
        )
        self.assertEqual(len(invitations), 0)
