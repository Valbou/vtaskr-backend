from unittest.mock import MagicMock

from src.users.managers import GroupManager
from src.users.models import Group
from tests.base_test import DummyBaseTestCase


class TestGroupManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.group_m = GroupManager(services=self.app.dependencies)

    def _get_group(self):
        return Group(name="Test Group", is_private=False)

    def test_create_group(self):
        self.group_m.group_db.save = MagicMock()

        group = self.group_m.create_group(session=None, group_name="MyGroup")

        self.group_m.group_db.save.assert_called_once()
        self.assertEqual(group.name, "MyGroup")

    def test_get_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=True)
        self.group_m.group_db.load = MagicMock(return_value=group)

        user_group = self.group_m.get_group(user_id="user_123", group_id=group.id)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.load.assert_called_once()

        self.assertEqual(group.id, user_group.id)

    def test_cannot_get_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=False)
        self.group_m.group_db.load = MagicMock(return_value=group)

        user_group = self.group_m.get_group(user_id="user_123", group_id=group.id)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.load.assert_not_called()

        self.assertIsNone(user_group)

    def test_update_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=True)
        self.group_m.group_db.save = MagicMock()

        updated = self.group_m.update_group(user_id="user_123", group=group)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.save.assert_called_once()

        self.assertTrue(updated)

    def test_cannot_update_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=False)
        self.group_m.group_db.save = MagicMock()

        updated = self.group_m.update_group(user_id="user_123", group=group)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.save.assert_not_called()

        self.assertFalse(updated)

    def test_delete_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=True)
        self.group_m.group_db.delete = MagicMock()

        deleted = self.group_m.delete_group(user_id="user_123", group=group)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.delete.assert_called_once()

        self.assertTrue(deleted)

    def test_cannot_delete_group(self):
        group = self._get_group()

        self.group_m.services.identity.can = MagicMock(return_value=False)
        self.group_m.group_db.delete = MagicMock()

        deleted = self.group_m.delete_group(user_id="user_123", group=group)

        self.group_m.services.identity.can.assert_called_once()
        self.group_m.group_db.delete.assert_not_called()

        self.assertFalse(deleted)

    def test_get_all_groups(self):
        self.group_m.group_db.get_all_user_groups = MagicMock(return_value=[])

        user_groups = self.group_m.get_all_groups(user_id="user_123")

        self.group_m.group_db.get_all_user_groups.assert_called_once()
        self.assertIsInstance(user_groups, list)
