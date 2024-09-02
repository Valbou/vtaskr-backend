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
        self.tag_m.tag_db.save = MagicMock()
        tag = self._get_tag()

        result = self.tag_m.create_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.tag_db.save.assert_called_once()
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

    def test_delete_tag(self):
        tag = self._get_tag()

        self.tag_m.services.identity.can = MagicMock(return_value=True)
        self.tag_m.tag_db.delete = MagicMock()

        result = self.tag_m.delete_tag(session=None, user_id="user_123", tag=tag)

        self.tag_m.services.identity.can.assert_called_once()
        self.tag_m.tag_db.delete.assert_called_once()

        self.assertTrue(result)
