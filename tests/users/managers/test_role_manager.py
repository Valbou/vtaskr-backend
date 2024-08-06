from unittest.mock import MagicMock

from src.users.managers import RoleManager
from src.users.models import Role
from tests.base_test import DummyBaseTestCase


class TestRoleManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.role_m = RoleManager(services=self.app.dependencies)

    def _get_role(self) -> Role:
        return Role(
            user_id="user_123", group_id="group_123", roletype_id="roletype_123"
        )

    def test_create_role(self):
        role = self._get_role()
        self.role_m.services.identity.can = MagicMock(return_value=True)
        self.role_m.role_db.save = MagicMock()

        new_role = self.role_m.create_role(user_id="user_123", role=role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.save.assert_called_once()

        self.assertEqual(new_role.user_id, "user_123")
        self.assertEqual(new_role.group_id, "group_123")
        self.assertEqual(new_role.roletype_id, "roletype_123")

    def test_cannot_create_role(self):
        role = self._get_role()
        self.role_m.services.identity.can = MagicMock(return_value=False)
        self.role_m.role_db.save = MagicMock()

        new_role = self.role_m.create_role(user_id="user_123", role=role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.save.assert_not_called()
        self.assertIsNone(new_role)

    def test_add_role(self):
        self.role_m.role_db.save = MagicMock()

        with self.app.dependencies.persistence.get_session() as session:
            role = self.role_m.add_role(
                session=session, user_id="a1", group_id="b2", roletype_id="c3"
            )

        self.role_m.role_db.save.assert_called_once()
        self.assertEqual(role.user_id, "a1")
        self.assertEqual(role.group_id, "b2")
        self.assertEqual(role.roletype_id, "c3")

    def test_get_role(self):
        base_role = self._get_role()
        self.role_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.role_m.role_db.get_a_user_role = MagicMock(return_value=base_role)

        role = self.role_m.get_role(user_id="user_123", role_id="role_123")

        self.role_m.services.identity.all_tenants_with_access.assert_called_once()
        self.role_m.role_db.get_a_user_role.assert_called_once()
        self.assertEqual(base_role.id, role.id)

    def test_get_all_roles(self):
        base_role = self._get_role()
        self.role_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.role_m.role_db.get_all_user_roles = MagicMock(return_value=[base_role])

        roles = self.role_m.get_all_roles(user_id="user_123")

        self.role_m.services.identity.all_tenants_with_access.assert_called_once()
        self.role_m.role_db.get_all_user_roles.assert_called_once()
        self.assertIsInstance(roles, list)
        role = roles[0]
        self.assertEqual(base_role.id, role.id)

    def test_get_all_roles_no_roles(self):
        self.role_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.role_m.role_db.get_all_user_roles = MagicMock(return_value=[])

        roles = self.role_m.get_all_roles(user_id="user_123")

        self.role_m.services.identity.all_tenants_with_access.assert_called_once()
        self.role_m.role_db.get_all_user_roles.assert_called_once()
        self.assertIsInstance(roles, list)
        self.assertEqual(len(roles), 0)

    def test_get_members(self):
        self.role_m.services.identity.can = MagicMock(return_value=True)
        self.role_m.role_db.get_group_roles = MagicMock(return_value=[])

        roles = self.role_m.get_members(user_id="user_123", group_id="group_123")

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.get_group_roles.assert_called_once()

        self.assertIsInstance(roles, list)

    def test_update_role(self):
        base_role = self._get_role()

        self.role_m.role_db.save = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=True)

        udpated = self.role_m.update_role(user_id="user_987", role=base_role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.save.assert_called_once()
        self.assertTrue(udpated)

    def test_cannot_update_role(self):
        base_role = self._get_role()

        self.role_m.role_db.save = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=False)

        udpated = self.role_m.update_role(user_id="user_987", role=base_role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.save.assert_not_called()
        self.assertFalse(udpated)

    def test_cannot_update_self_role(self):
        base_role = self._get_role()

        self.role_m.role_db.save = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=False)

        udpated = self.role_m.update_role(user_id="user_123", role=base_role)

        self.role_m.services.identity.can.assert_not_called()
        self.role_m.role_db.save.assert_not_called()
        self.assertFalse(udpated)

    def test_delete_role(self):
        base_role = self._get_role()

        self.role_m.role_db.delete = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=True)

        deleted = self.role_m.delete_role(user_id="user_987", role=base_role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.delete.assert_called_once()
        self.assertTrue(deleted)

    def test_cannot_delete_role(self):
        base_role = self._get_role()

        self.role_m.role_db.delete = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=False)

        deleted = self.role_m.delete_role(user_id="user_987", role=base_role)

        self.role_m.services.identity.can.assert_called_once()
        self.role_m.role_db.delete.assert_not_called()
        self.assertFalse(deleted)

    def test_cannot_delete_self_role(self):
        base_role = self._get_role()

        self.role_m.role_db.delete = MagicMock()
        self.role_m.services.identity.can = MagicMock(return_value=False)

        deleted = self.role_m.delete_role(user_id="user_123", role=base_role)

        self.role_m.services.identity.can.assert_not_called()
        self.role_m.role_db.delete.assert_not_called()
        self.assertFalse(deleted)
