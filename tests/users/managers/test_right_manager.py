from unittest.mock import MagicMock

from src.libs.iam.constants import Permissions
from src.users.managers import RightManager
from src.users.models import Right, RoleType
from tests.base_test import DummyBaseTestCase


class TestRightManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.right_m = RightManager(services=self.app.dependencies)

    def _get_right(self) -> Right:
        return Right(
            roletype_id="roletype_123",
            resource="Test",
            permissions=[Permissions.SUSCRIBE, Permissions.EXECUTE],
        )

    def _get_roletype(self) -> RoleType:
        return RoleType(id="roletype_123", name="My Role", group_id="group_123")

    def test_create_observer_rights(self):
        roletype = self._get_roletype()
        self.right_m.right_db.save = MagicMock()

        num_results = self.right_m.create_observer_rights(roletype=roletype)

        self.right_m.right_db.save.assert_called()

        self.assertEqual(
            len(self.app.dependencies.identity.get_resources()), num_results
        )

    def test_create_admin_rights(self):
        roletype = self._get_roletype()
        self.right_m.right_db.save = MagicMock()

        num_results = self.right_m.create_admin_rights(
            session=None, roletype_id=roletype.id
        )

        self.right_m.right_db.save.assert_called()

        self.assertEqual(
            len(self.app.dependencies.identity.get_resources()), num_results
        )

    def test_add_right(self):
        self.right_m.right_db.save = MagicMock()

        new_right = self.right_m.add_right(
            roletype_id="roletype_123",
            resource="GROUP",
            permissions=Permissions.SUSCRIBE,
        )

        self.right_m.right_db.save.assert_called_once()

        self.assertEqual(new_right.roletype_id, "roletype_123")
        self.assertEqual(new_right.resource, "GROUP")
        self.assertEqual(new_right.permissions, [Permissions.SUSCRIBE])

    def test_create_right(self):
        new_right = self._get_right()
        self.right_m.services.identity.can = MagicMock(return_value=True)
        self.right_m.right_db.save = MagicMock()

        right = self.right_m.create_right(
            user_id="user_123", group_id="group_123", right=new_right
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.save.assert_called_once()

        self.assertEqual(right.roletype_id, "roletype_123")
        self.assertEqual(right.resource, "Test")
        self.assertEqual(right.permissions, [Permissions.SUSCRIBE, Permissions.EXECUTE])

    def test_cannot_create_right(self):
        new_right = self._get_right()
        self.right_m.services.identity.can = MagicMock(return_value=False)
        self.right_m.right_db.save = MagicMock()

        right = self.right_m.create_right(
            user_id="user_123", group_id="group_123", right=new_right
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.save.assert_not_called()

        self.assertIsNone(right)

    def test_get_right(self):
        right = self._get_right()

        self.right_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.right_m.right_db.get_a_user_right = MagicMock(return_value=right)

        user_right = self.right_m.get_right(user_id="user_123", right_id=right.id)

        self.right_m.services.identity.all_tenants_with_access.assert_called_once()
        self.right_m.right_db.get_a_user_right.assert_called_once()

        self.assertEqual(right.id, user_right.id)

    def test_cannot_get_right(self):
        right = self._get_right()

        self.right_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.right_m.right_db.get_a_user_right = MagicMock(return_value=None)

        user_right = self.right_m.get_right(user_id="user_123", right_id=right.id)

        self.right_m.services.identity.all_tenants_with_access.assert_called_once()
        self.right_m.right_db.get_a_user_right.assert_called_once()

        self.assertIsNone(user_right)

    def test_get_all_rights(self):
        right = self._get_right()

        self.right_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.right_m.right_db.get_all_user_rights = MagicMock(return_value=[right])

        user_rights = self.right_m.get_all_rights(user_id="user_132")

        self.right_m.services.identity.all_tenants_with_access.assert_called_once()
        self.right_m.right_db.get_all_user_rights.assert_called_once()

        self.assertIsInstance(user_rights, list)
        user_right = user_rights[0]

        self.assertEqual(right.id, user_right.id)

    def test_update_right(self):
        base_right = self._get_right()
        base_roletype = self._get_roletype()

        self.right_m.right_db.save = MagicMock()
        self.right_m.services.identity.can = MagicMock(return_value=True)

        udpated = self.right_m.update_right(
            user_id="user_123", right=base_right, roletype=base_roletype
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.save.assert_called_once()
        self.assertTrue(udpated)

    def test_cannot_update_right(self):
        base_right = self._get_right()
        base_roletype = self._get_roletype()

        self.right_m.right_db.save = MagicMock()
        self.right_m.services.identity.can = MagicMock(return_value=False)

        udpated = self.right_m.update_right(
            user_id="user_123", right=base_right, roletype=base_roletype
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.save.assert_not_called()
        self.assertFalse(udpated)

    def test_delete_right(self):
        base_right = self._get_right()
        base_roletype = self._get_roletype()

        self.right_m.right_db.delete = MagicMock()
        self.right_m.services.identity.can = MagicMock(return_value=True)

        deleted = self.right_m.delete_right(
            user_id="user_123", right=base_right, roletype=base_roletype
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.delete.assert_called_once()
        self.assertTrue(deleted)

    def test_cannot_delete_right(self):
        base_right = self._get_right()
        base_roletype = self._get_roletype()

        self.right_m.right_db.delete = MagicMock()
        self.right_m.services.identity.can = MagicMock(return_value=False)

        deleted = self.right_m.delete_right(
            user_id="user_123", right=base_right, roletype=base_roletype
        )

        self.right_m.services.identity.can.assert_called_once()
        self.right_m.right_db.delete.assert_not_called()
        self.assertFalse(deleted)
