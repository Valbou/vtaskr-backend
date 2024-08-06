from unittest.mock import MagicMock

from src.users.managers import InvitationManager
from src.users.models import Invitation
from tests.base_test import DummyBaseTestCase


class TestInvitationManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.invitation_m = InvitationManager(services=self.app.dependencies)

    def _get_invitation(self) -> Invitation:
        return Invitation(
            from_user_id="user_123",
            to_user_email="test@example.com",
            with_roletype_id="roletype_123",
            in_group_id="group_123",
        )

    def test_clean_expired(self):
        self.invitation_m.invitation_db.clean_expired = MagicMock()

        self.invitation_m.clean_expired(session=None)

        self.invitation_m.invitation_db.clean_expired.assert_called_once()

    def test_get_invitation(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.load = MagicMock(return_value=base_invitation)

        invitation = self.invitation_m.get_invitation(
            session=None, invitation_id="invitation_123"
        )

        self.invitation_m.invitation_db.load.assert_called_once()

        self.assertIsInstance(invitation, Invitation)
        self.assertEqual(base_invitation.id, invitation.id)

    def test_get_from_hash(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.get_from_hash = MagicMock(
            return_value=base_invitation
        )

        invitation = self.invitation_m.get_from_hash(session=None, hash="hash_123")

        self.invitation_m.invitation_db.get_from_hash.assert_called_once()

        self.assertIsInstance(invitation, Invitation)
        self.assertEqual(base_invitation.id, invitation.id)

    def test_get_from_group(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.get_from_group = MagicMock(
            return_value=[base_invitation]
        )
        self.invitation_m.services.identity.can = MagicMock(return_value=True)

        invitations = self.invitation_m.get_from_group(
            session=None, user_id="user_123", group_id="group_123"
        )

        self.invitation_m.invitation_db.get_from_group.assert_called_once()

        self.assertIsInstance(invitations, list)
        invitation = invitations[0]
        self.assertIsInstance(invitation, Invitation)
        self.assertEqual(base_invitation.id, invitation.id)

    def test_cannot_get_from_group(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.get_from_group = MagicMock(
            return_value=[base_invitation]
        )
        self.invitation_m.services.identity.can = MagicMock(return_value=False)

        invitations = self.invitation_m.get_from_group(
            session=None, user_id="user_123", group_id="group_123"
        )

        self.invitation_m.invitation_db.get_from_group.assert_not_called()

        self.assertIsInstance(invitations, list)
        self.assertEqual(len(invitations), 0)

    def test_update_invitation(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.save = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=True)

        result = self.invitation_m.update_invitation(
            session=None, user_id="user_123", invitation=base_invitation
        )

        self.invitation_m.invitation_db.save.assert_called_once()

        self.assertTrue(result)

    def test_cannot_update_invitation(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.save = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=False)

        result = self.invitation_m.update_invitation(
            session=None, user_id="user_123", invitation=base_invitation
        )

        self.invitation_m.invitation_db.save.assert_not_called()

        self.assertFalse(result)

    def test_delete_invitation(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.delete = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=True)

        result = self.invitation_m.delete_invitation(
            session=None, user_id="user_123", invitation=base_invitation
        )

        self.invitation_m.invitation_db.delete.assert_called_once()
        self.assertTrue(result)

    def test_cannot_delete_invitation(self):
        base_invitation = self._get_invitation()
        self.invitation_m.invitation_db.delete = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=False)

        result = self.invitation_m.delete_invitation(
            session=None, user_id="user_123", invitation=base_invitation
        )

        self.invitation_m.invitation_db.delete.assert_not_called()
        self.assertFalse(result)

    def test_delete_invitation_by_id(self):
        self.invitation_m.invitation_db.delete_by_id = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=True)

        result = self.invitation_m.delete_invitation_by_id(
            session=None,
            user_id="user_123",
            group_id="group_123",
            invitation_id="invitation_123",
        )

        self.invitation_m.invitation_db.delete_by_id.assert_called_once()
        self.assertTrue(result)

    def test_cannot_delete_invitation_by_id(self):
        self.invitation_m.invitation_db.delete_by_id = MagicMock()
        self.invitation_m.services.identity.can = MagicMock(return_value=False)

        result = self.invitation_m.delete_invitation_by_id(
            session=None,
            user_id="user_123",
            group_id="group_123",
            invitation_id="invitation_123",
        )

        self.invitation_m.invitation_db.delete_by_id.assert_not_called()
        self.assertFalse(result)
