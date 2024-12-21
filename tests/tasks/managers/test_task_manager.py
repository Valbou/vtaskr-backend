from unittest.mock import MagicMock

from src.tasks.managers import TaskManager
from src.tasks.models import Task
from tests.base_test import DummyBaseTestCase


class TestTaskManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.task_m = TaskManager(services=self.app.dependencies)

    def _get_task(self) -> Task:
        return Task(
            title="Test Task",
            tenant_id="tenant_123",
        )

    def test_create_task(self):
        self.task_m.services.identity.can = MagicMock(return_value=True)
        self.task_m.task_db.save = MagicMock()
        task = self._get_task()

        result = self.task_m.create_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.save.assert_called_once()
        self.assertTrue(result)

    def test_cannot_create_task(self):
        self.task_m.services.identity.can = MagicMock(return_value=False)
        self.task_m.task_db.save = MagicMock()
        task = self._get_task()

        result = self.task_m.create_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.save.assert_not_called()
        self.assertFalse(result)

    def test_get_task(self):
        base_task = self._get_task()

        self.task_m.task_db.load = MagicMock(return_value=base_task)
        self.task_m.services.identity.can = MagicMock(return_value=True)

        task = self.task_m.get_task(
            session=None, user_id="user_123", task_id="task_123"
        )

        self.task_m.task_db.load.assert_called_once()
        self.task_m.services.identity.can.assert_called_once()

        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "Test Task")

    def test_get_no_task(self):
        base_task = self._get_task()

        self.task_m.task_db.load = MagicMock(return_value=None)
        self.task_m.services.identity.can = MagicMock(return_value=True)

        task = self.task_m.get_task(
            session=None, user_id="user_123", task_id="task_123"
        )

        self.task_m.task_db.load.assert_called_once()
        self.task_m.services.identity.can.assert_not_called()

        self.assertIsNone(task)

    def test_get_tasks(self):
        task = self._get_task()

        self.task_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=["tenant_123"]
        )
        self.task_m.task_db.tasks = MagicMock(return_value=[task])

        tasks = self.task_m.get_tasks(session=None, user_id="user_123")

        self.task_m.services.identity.all_tenants_with_access.assert_called_once()
        self.task_m.task_db.tasks.assert_called_once()

        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 1)
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(tasks[0].title, "Test Task")

    def test_get_tag_tasks(self):
        task = self._get_task()

        self.task_m.services.identity.all_tenants_with_access = MagicMock(
            return_value=["tenant_123"]
        )
        self.task_m.task_db.tag_tasks = MagicMock(return_value=[task])

        tasks = self.task_m.get_tag_tasks(
            session=None, user_id="user_123", tag_id="tag_123"
        )

        self.task_m.services.identity.all_tenants_with_access.assert_called_once()
        self.task_m.task_db.tag_tasks.assert_called_once_with(
            session=None, tenant_ids=["tenant_123"], tag_id="tag_123", qs_filters=None
        )

        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 1)
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(tasks[0].title, "Test Task")

    def test_update_task(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=True)
        self.task_m.task_db.save = MagicMock()

        result = self.task_m.update_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.save.assert_called_once()

        self.assertTrue(result)

    def test_cannot_update_task(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=False)
        self.task_m.task_db.save = MagicMock()

        result = self.task_m.update_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.save.assert_not_called()

        self.assertFalse(result)

    def test_clean_task_tags(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=True)
        self.task_m.task_db.clean_tags = MagicMock()

        result = self.task_m.clean_task_tags(
            session=None, user_id="user_123", task=task
        )

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.clean_tags.assert_called_once()

        self.assertTrue(result)

    def test_cannot_clean_task_tags(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=False)
        self.task_m.task_db.clean_tags = MagicMock()

        result = self.task_m.clean_task_tags(
            session=None, user_id="user_123", task=task
        )

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.clean_tags.assert_not_called()

        self.assertFalse(result)

    def test_delete_task(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=True)
        self.task_m.task_db.delete = MagicMock()

        result = self.task_m.delete_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.delete.assert_called_once()

        self.assertTrue(result)

    def test_cannot_delete_task(self):
        task = self._get_task()

        self.task_m.services.identity.can = MagicMock(return_value=False)
        self.task_m.task_db.delete = MagicMock()

        result = self.task_m.delete_task(session=None, user_id="user_123", task=task)

        self.task_m.services.identity.can.assert_called_once()
        self.task_m.task_db.delete.assert_not_called()

        self.assertFalse(result)

    def test_delete_all_tenant_tasks(self):
        self.task_m.task_db.delete_all_by_tenant = MagicMock()

        self.task_m.delete_all_tenant_tasks(session=None, tenant_id="tenant_123")

        self.task_m.task_db.delete_all_by_tenant.assert_called_once_with(
            session=None, tenant_id="tenant_123"
        )
