from unittest.mock import MagicMock

from src.users.managers import RoleTypeManager
from src.users.models import RoleType
from tests.base_test import DummyBaseTestCase


class TestRoleTypeManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.roletype_m = RoleTypeManager(services=self.app.dependencies)

    def _get_observer_roletype(self) -> RoleType:
        return RoleType(name="Observer", group_id=None)

    def _get_admin_roletype(self) -> RoleType:
        return RoleType(name="Admin", group_id=None)

    def _get_other_roletype(self) -> RoleType:
        return RoleType(name="My Role", group_id="group_123")

    def test_get_default_observer(self):
        base_roletype = self._get_observer_roletype()
        self.roletype_m.roletype_db.get_or_create = MagicMock(
            return_value=(base_roletype, True)
        )

        roletype, created = self.roletype_m.get_default_observer()

        self.roletype_m.roletype_db.get_or_create.assert_called_once()

        self.assertTrue(created)
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, "Observer")
        self.assertEqual(roletype.group_id, None)

    def test_get_default_observer_already_exists(self):
        roletype = self._get_observer_roletype()
        self.roletype_m.roletype_db.get_or_create = MagicMock(
            return_value=(roletype, False)
        )

        roletype, created = self.roletype_m.get_default_observer()

        self.roletype_m.roletype_db.get_or_create.assert_called_once()

        self.assertFalse(created)
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, "Observer")
        self.assertEqual(roletype.group_id, None)

    def test_get_default_admin(self):
        base_roletype = self._get_admin_roletype()
        self.roletype_m.roletype_db.get_or_create = MagicMock(
            return_value=(base_roletype, True)
        )

        roletype, created = self.roletype_m.get_default_admin()

        self.roletype_m.roletype_db.get_or_create.assert_called_once()

        self.assertTrue(created)
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, "Admin")
        self.assertEqual(roletype.group_id, None)

    def test_get_default_admin_already_exists(self):
        roletype = self._get_admin_roletype()
        self.roletype_m.roletype_db.get_or_create = MagicMock(
            return_value=(roletype, False)
        )

        roletype, created = self.roletype_m.get_default_admin()

        self.roletype_m.roletype_db.get_or_create.assert_called_once()

        self.assertFalse(created)
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, "Admin")
        self.assertEqual(roletype.group_id, None)

    def test_create_custom_roletype(self):
        base_roletype = self._get_other_roletype()
        self.roletype_m.roletype_db.get_or_create = MagicMock(
            return_value=(base_roletype, True)
        )

        roletype, created = self.roletype_m.create_custom_roletype(
            name=base_roletype.name, group_id=base_roletype.group_id
        )

        self.roletype_m.roletype_db.get_or_create.assert_called_once()

        self.assertTrue(created)
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, base_roletype.name)
        self.assertEqual(roletype.group_id, base_roletype.group_id)

    def test_get_roletype(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.get_a_user_roletype = MagicMock(
            return_value=base_roletype
        )
        self.roletype_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )

        roletype = self.roletype_m.get_roletype(
            user_id="user_123", roletype_id="roletype_123"
        )

        self.roletype_m.roletype_db.get_a_user_roletype.assert_called_once()
        self.roletype_m.services.identity.all_tenants_with_access.assert_called_once()

        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, base_roletype.name)
        self.assertEqual(roletype.group_id, base_roletype.group_id)

    def test_get_all_roletypes(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.get_all_user_roletypes = MagicMock(
            return_value=[base_roletype]
        )
        self.roletype_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )

        roletypes_list = self.roletype_m.get_all_roletypes(user_id="user_123")

        self.roletype_m.roletype_db.get_all_user_roletypes.assert_called_once()
        self.roletype_m.services.identity.all_tenants_with_access.assert_called_once()

        self.assertIsInstance(roletypes_list, list)
        roletype = roletypes_list[0]

        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, base_roletype.name)
        self.assertEqual(roletype.group_id, base_roletype.group_id)

    def test_update_roletype(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.save = MagicMock()
        self.roletype_m.services.identity.can = MagicMock(return_value=True)

        updated = self.roletype_m.update_roletype(
            user_id="user_123", roletype=base_roletype
        )

        self.roletype_m.services.identity.can.assert_called_once()
        self.roletype_m.roletype_db.save.assert_called_once()
        self.assertTrue(updated)

    def test_cannot_update_roletype(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.save = MagicMock()
        self.roletype_m.services.identity.can = MagicMock(return_value=False)

        updated = self.roletype_m.update_roletype(
            user_id="user_123", roletype=base_roletype
        )

        self.roletype_m.services.identity.can.assert_called_once()
        self.roletype_m.roletype_db.save.assert_not_called()
        self.assertFalse(updated)

    def test_delete_roletype(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.delete = MagicMock()
        self.roletype_m.services.identity.can = MagicMock(return_value=True)

        deleted = self.roletype_m.delete_roletype(
            user_id="user_123", roletype=base_roletype
        )

        self.roletype_m.services.identity.can.assert_called_once()
        self.roletype_m.roletype_db.delete.assert_called_once()
        self.assertTrue(deleted)

    def test_cannot_delete_roletype(self):
        base_roletype = self._get_other_roletype()

        self.roletype_m.roletype_db.delete = MagicMock()
        self.roletype_m.services.identity.can = MagicMock(return_value=False)

        deleted = self.roletype_m.delete_roletype(
            user_id="user_123", roletype=base_roletype
        )

        self.roletype_m.services.identity.can.assert_called_once()
        self.roletype_m.roletype_db.delete.assert_not_called()
        self.assertFalse(deleted)
