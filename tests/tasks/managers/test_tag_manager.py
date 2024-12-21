from unittest.mock import MagicMock

from src.tasks.managers import TagManager
from src.tasks.models import Tag
from tests.base_test import DummyBaseTestCase


class TestTagManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tag_m = TagManager(services=self.app.dependencies)

    def _get_tag(self) -> Tag:
        return Tag(
            title="Test Tag",
            tenant_id="tenant_123",
        )

    def test_create_tag(self):
        self.tag_m.services.identity.can = MagicMock(return_value=True)
        self.tag_m.tag_db.save = MagicMock()
        tag = self._get_tag()

        result = self.tag_m.create_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.save.assert_called_once()
        self.assertTrue(result)

    def test_cannot_create_tag(self):
        self.tag_m.services.identity.can = MagicMock(return_value=False)
        self.tag_m.tag_db.save = MagicMock()
        tag = self._get_tag()

        result = self.tag_m.create_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.save.assert_not_called()
        self.assertFalse(result)

    def test_tags_exists(self):
        self.tag_m.services.identity.all_tenants_with_access = MagicMock()
        self.tag_m.tag_db.all_exists = MagicMock(return_value=True)

        result = self.tag_m.tags_exists(
            session=None, user_id="user_123", tag_ids=["tag_123"]
        )

        self.tag_m.services.identity.all_tenants_with_access.assert_called_once()
        self.tag_m.tag_db.all_exists.assert_called_once()

        self.assertTrue(result)

    def test_get_tag(self):
        base_tag = self._get_tag()

        self.tag_m.tag_db.load = MagicMock(return_value=base_tag)
        self.tag_m.services.identity.can = MagicMock(return_value=True)

        tag = self.tag_m.get_tag(session=None, user_id="user_123", tag_id="tag_123")

        self.tag_m.tag_db.load.assert_called_once()
        self.tag_m.services.identity.can.assert_called_once()

        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.title, "Test Tag")

    def test_cannot_get_tag(self):
        self.tag_m.tag_db.load = MagicMock(return_value=None)
        self.tag_m.services.identity.can = MagicMock(return_value=False)

        tag = self.tag_m.get_tag(session=None, user_id="user_123", tag_id="tag_123")

        self.tag_m.tag_db.load.assert_called_once()
        self.tag_m.services.identity.can.assert_not_called()

        self.assertIsNone(tag)

    def test_get_tags(self):
        tag = self._get_tag()

        self.tag_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=["tenant_123"]
        )
        self.tag_m.tag_db.tags = MagicMock(return_value=[tag])

        tags = self.tag_m.get_tags(session=None, user_id="user_123")

        self.tag_m.services.identity.all_tenants_with_access.assert_called_once()
        self.tag_m.tag_db.tags.assert_called_once()

        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 1)
        self.assertIsInstance(tags[0], Tag)
        self.assertEqual(tags[0].title, "Test Tag")

    def test_get_tags_from_ids(self):
        self.tag_m.services.identity.all_tenants_with_access = MagicMock()
        self.tag_m.tag_db.tags_from_ids = MagicMock(return_value=[])

        result = self.tag_m.get_tags_from_ids(
            session=None, user_id="user_123", tag_ids=["tag_123"]
        )

        self.tag_m.services.identity.all_tenants_with_access.assert_called_once()
        self.tag_m.tag_db.tags_from_ids.assert_called_once()

        self.assertIsInstance(result, list)

    def test_get_task_tags(self):
        tag = self._get_tag()

        self.tag_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=["tenant_123"]
        )
        self.tag_m.tag_db.task_tags = MagicMock(return_value=[tag])

        tags = self.tag_m.get_task_tags(
            session=None, user_id="user_123", task_id="task_123"
        )

        self.tag_m.services.identity.all_tenants_with_access.assert_called_once()
        self.tag_m.tag_db.task_tags.assert_called_once_with(
            session=None, tenant_ids=["tenant_123"], task_id="task_123"
        )

        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 1)
        self.assertIsInstance(tags[0], Tag)
        self.assertEqual(tags[0].title, "Test Tag")

    def test_update_tag(self):
        tag = self._get_tag()

        self.tag_m.services.identity.can = MagicMock(return_value=True)
        self.tag_m.tag_db.save = MagicMock()

        result = self.tag_m.update_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.save.assert_called_once()

        self.assertTrue(result)

    def test_cannot_update_tag(self):
        tag = self._get_tag()

        self.tag_m.services.identity.can = MagicMock(return_value=False)
        self.tag_m.tag_db.save = MagicMock()

        result = self.tag_m.update_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.save.assert_not_called()

        self.assertFalse(result)

    def test_delete_tag(self):
        tag = self._get_tag()

        self.tag_m.services.identity.can = MagicMock(return_value=True)
        self.tag_m.tag_db.delete = MagicMock()

        result = self.tag_m.delete_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.delete.assert_called_once()

        self.assertTrue(result)

    def test_cannot_delete_tag(self):
        tag = self._get_tag()

        self.tag_m.services.identity.can = MagicMock(return_value=False)
        self.tag_m.tag_db.delete = MagicMock()

        result = self.tag_m.delete_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.delete.assert_not_called()

        self.assertFalse(result)

    def test_delete_all_tenant_tags(self):
        self.tag_m.tag_db.delete_all_by_tenant = MagicMock()

        self.tag_m.delete_all_tenant_tags(session=None, tenant_id="tenant_123")

        self.tag_m.tag_db.delete_all_by_tenant.assert_called_once_with(
            session=None, tenant_id="tenant_123"
        )
