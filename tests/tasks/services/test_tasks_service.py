from datetime import datetime
from unittest.mock import ANY, MagicMock

from src.tasks.models import Tag, Task
from src.tasks.services import TasksService
from tests.base_test import DummyBaseTestCase


class TestTasksService(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.tasks_service = TasksService(services=self.app.dependencies)

    def _get_task(self) -> Task:
        return Task(title="Test Task", tenant_id="tenant_123")

    def _get_tag(self) -> Tag:
        return Tag(title="Test Tag", tenant_id="tenant_123")

    def test_create_new_task(self):
        base_task = self._get_task()
        self.tasks_service.task_manager.create_task = MagicMock(return_value=True)

        result = self.tasks_service.create_new_task(user_id="user_123", task=base_task)

        self.tasks_service.task_manager.create_task.assert_called_once()

        self.assertTrue(result)

    def test_get_user_task(self):
        base_task = self._get_task()

        self.tasks_service.task_manager.get_task = MagicMock(return_value=base_task)

        task = self.tasks_service.get_user_task(user_id="user_123", task_id="task_123")

        self.tasks_service.task_manager.get_task.assert_called_once()

        self.assertIsInstance(task, Task)
        self.assertEqual(task.id, base_task.id)

    def test_get_user_all_tasks(self):
        base_task = self._get_task()

        self.tasks_service.task_manager.get_tasks = MagicMock(
            return_value=[base_task, base_task]
        )

        tasks = self.tasks_service.get_user_all_tasks(user_id="user_123")

        self.tasks_service.task_manager.get_tasks.assert_called_once()

        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 2)
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(tasks[0].id, base_task.id)

    def test_get_all_tag_tasks(self):
        self.tasks_service.task_manager.get_tag_tasks = MagicMock(return_value=[])

        result = self.tasks_service.get_all_tag_tasks(
            user_id="user_123", tag_id="tag_123"
        )

        self.assertIsInstance(result, list)

        self.tasks_service.task_manager.get_tag_tasks.assert_called_once()

    def test_update_task(self):
        base_task = self._get_task()

        self.tasks_service.task_manager.update_task = MagicMock(return_value=True)

        result = self.tasks_service.update_task(user_id="user_123", task=base_task)

        self.tasks_service.task_manager.update_task.assert_called_once()

        self.assertTrue(result)

    def test_delete_task(self):
        base_task = self._get_task()

        self.tasks_service.task_manager.delete_task = MagicMock(return_value=True)

        result = self.tasks_service.delete_task(user_id="user_123", task=base_task)

        self.tasks_service.task_manager.delete_task.assert_called_once()

        self.assertTrue(result)

    def test_create_new_tag(self):
        base_tag = self._get_tag()
        self.tasks_service.tag_manager.create_tag = MagicMock(return_value=True)

        result = self.tasks_service.create_new_tag(user_id="user_123", tag=base_tag)

        self.tasks_service.tag_manager.create_tag.assert_called_once()

        self.assertTrue(result)

    def test_get_user_tag(self):
        base_tag = self._get_tag()

        self.tasks_service.tag_manager.get_tag = MagicMock(return_value=base_tag)

        tag = self.tasks_service.get_user_tag(user_id="user_123", tag_id="tag_123")

        self.tasks_service.tag_manager.get_tag.assert_called_once()

        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.id, base_tag.id)

    def test_check_user_tag_exists(self):
        self.tasks_service.tag_manager.tags_exists = MagicMock(return_value=True)

        result = self.tasks_service.check_user_tag_exists(
            user_id="user_123", tag_id="tag_123"
        )

        self.assertIsInstance(result, bool)
        self.assertTrue(result)

        self.tasks_service.tag_manager.tags_exists.assert_called_once()

    def test_get_all_task_tags(self):
        self.tasks_service.tag_manager.get_task_tags = MagicMock(return_value=[])

        result = self.tasks_service.get_all_task_tags(
            user_id="user_123", task_id="task_123"
        )

        self.assertIsInstance(result, list)

        self.tasks_service.tag_manager.get_task_tags.assert_called_once()

    def test_get_tags_from_id(self):
        self.tasks_service.tag_manager.get_tags_from_ids = MagicMock(return_value=[])

        result = self.tasks_service.get_tags_from_id(
            user_id="user_123", tag_ids=["tag_123"]
        )

        self.assertIsInstance(result, list)

        self.tasks_service.tag_manager.get_tags_from_ids.assert_called_once()

    def test_get_user_all_tags(self):
        base_tag = self._get_tag()

        self.tasks_service.tag_manager.get_tags = MagicMock(
            return_value=[base_tag, base_tag]
        )

        tags = self.tasks_service.get_user_all_tags(user_id="user_123")

        self.tasks_service.tag_manager.get_tags.assert_called_once()

        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 2)
        self.assertIsInstance(tags[0], Tag)
        self.assertEqual(tags[0].id, base_tag.id)

    def test_update_tag(self):
        base_tag = self._get_tag()

        self.tasks_service.tag_manager.update_tag = MagicMock(return_value=True)

        result = self.tasks_service.update_tag(user_id="user_123", tag=base_tag)

        self.tasks_service.tag_manager.update_tag.assert_called_once()

        self.assertTrue(result)

    def test_delete_tag(self):
        base_tag = self._get_tag()

        self.tasks_service.tag_manager.delete_tag = MagicMock(return_value=True)

        result = self.tasks_service.delete_tag(user_id="user_123", tag=base_tag)

        self.tasks_service.tag_manager.delete_tag.assert_called_once()

        self.assertTrue(result)

    def test_set_tags_to_task(self):
        base_task = self._get_task()
        base_tag = self._get_tag()

        self.tasks_service.task_manager.get_task = MagicMock(return_value=base_task)
        self.tasks_service.get_tags_from_id = MagicMock(return_value=[base_tag])
        self.tasks_service.task_manager.update_task = MagicMock()

        result = self.tasks_service.set_tags_to_task(
            user_id="user_123", task_id="task_123", tag_ids=[base_tag.id]
        )

        self.assertTrue(result)

        self.tasks_service.task_manager.get_task.assert_called_once_with(
            user_id="user_123", task_id="task_123"
        )
        self.tasks_service.get_tags_from_id.assert_called_once()
        self.tasks_service.task_manager.update_task.assert_called_once()

    def test_set_tags_no_task(self):
        base_tag = self._get_tag()

        self.tasks_service.task_manager.get_task = MagicMock(return_value=None)
        self.tasks_service.get_tags_from_id = MagicMock()
        self.tasks_service.task_manager.update_task = MagicMock()

        result = self.tasks_service.set_tags_to_task(
            user_id="user_123", task_id="task_123", tag_ids=[base_tag.id]
        )

        self.assertFalse(result)

        self.tasks_service.task_manager.get_task.assert_called_once_with(
            user_id="user_123", task_id="task_123"
        )
        self.tasks_service.get_tags_from_id.assert_not_called()
        self.tasks_service.task_manager.update_task.assert_not_called()

    def test_unset_tags_to_task(self):
        base_task = self._get_task()
        base_tag = self._get_tag()

        self.tasks_service.task_manager.get_task = MagicMock(return_value=base_task)
        self.tasks_service.get_tags_from_id = MagicMock(return_value=[base_tag])
        self.tasks_service.task_manager.update_task = MagicMock()

        result = self.tasks_service.set_tags_to_task(
            user_id="user_123", task_id="task_123", tag_ids=[]
        )

        self.assertTrue(result)

        self.tasks_service.task_manager.get_task.assert_called_once_with(
            user_id="user_123", task_id="task_123"
        )
        self.tasks_service.get_tags_from_id.assert_not_called()
        self.tasks_service.task_manager.update_task.assert_called_once()

    def test_set_no_tags_to_task(self):
        base_task = self._get_task()
        base_tag = self._get_tag()

        self.tasks_service.task_manager.get_task = MagicMock(return_value=base_task)
        self.tasks_service.get_tags_from_id = MagicMock(return_value=[])
        self.tasks_service.task_manager.update_task = MagicMock()

        result = self.tasks_service.set_tags_to_task(
            user_id="user_123", task_id="task_123", tag_ids=[base_tag.id]
        )

        self.assertTrue(result)

        self.tasks_service.task_manager.get_task.assert_called_once_with(
            user_id="user_123", task_id="task_123"
        )
        self.tasks_service.get_tags_from_id.assert_called_once()
        self.tasks_service.task_manager.update_task.assert_called_once()

    def test_clean_all_items_of_tenant(self):
        self.tasks_service.task_manager.delete_all_tenant_tasks = MagicMock()
        self.tasks_service.tag_manager.delete_all_tenant_tags = MagicMock()

        self.tasks_service.clean_all_items_of_tenant(tenant_id="tenant_123")

        self.tasks_service.task_manager.delete_all_tenant_tasks.assert_called_once_with(
            session=ANY, tenant_id="tenant_123"
        )
        self.tasks_service.tag_manager.delete_all_tenant_tags.assert_called_once_with(
            session=ANY, tenant_id="tenant_123"
        )

    def test_add_tasks_dict_to_index(self):
        now = datetime.now()
        tasks = [
            Task(
                title="Test 1",
                tenant_id="tenant_123",
                assigned_to="assigned_123",
                scheduled_at=now,
            ),
            Task(
                title="Test 2",
                tenant_id="tenant_123",
                assigned_to="asssigned_456",
                scheduled_at=now,
            ),
            Task(
                title="Test 3",
                tenant_id="tenant_123",
                assigned_to="assigned_123",
                scheduled_at=now,
            ),
        ]

        index = {}
        self.tasks_service._add_tasks_dict_to_index(index=index, tasks=tasks)

        self.assertEqual(len(index.keys()), 2)
        self.assertIsInstance(index["assigned_123"], list)
        self.assertEqual(len(index["assigned_123"]), 2)
        self.assertIsInstance(index["asssigned_456"], list)
        self.assertEqual(len(index["asssigned_456"]), 1)

    def test_notify_tasks_to_assigned(self):
        now = datetime.now()
        self.tasks_service.task_manager.get_tasks_assigned_to_and_scheduled_between = (
            MagicMock(
                return_value=[
                    Task(
                        title="Test 1",
                        tenant_id="tenant_123",
                        assigned_to="assigned_123",
                        scheduled_at=now,
                    )
                ]
            )
        )
        self.tasks_service.event_manager.send_tasks_todo_today_event = MagicMock()

        self.tasks_service.notify_tasks_to_assigned(
            assigned_ids=["assigned_123"], now=now, end_day_1=now, end_day_2=now
        )

        total_calls = (
            self.tasks_service.task_manager.get_tasks_assigned_to_and_scheduled_between.call_count
        )
        self.assertEqual(total_calls, 2)
        (
            self.tasks_service.event_manager.send_tasks_todo_today_event.assert_called_once()
        )

    def test_notify_tasks_to_assigned_log_error(self):
        self.maxDiff = None

        now = datetime.now()
        self.tasks_service.task_manager.get_tasks_assigned_to_and_scheduled_between = (
            MagicMock(
                return_value=[
                    Task(
                        title="Test 1",
                        tenant_id="tenant_123",
                        assigned_to="assigned_123",
                        scheduled_at=now,
                    )
                ]
            )
        )

        self.tasks_service.event_manager.send_tasks_todo_today_event = MagicMock(
            side_effect=ValueError("Test")
        )

        with self.assertLogs("src.tasks.services.tasks_service", level="ERROR") as cm:
            self.tasks_service.notify_tasks_to_assigned(
                assigned_ids=["signed_123"], now=now, end_day_1=now, end_day_2=now
            )

            expected = "Tasks assigned notification error: Test - assigned to signed_123"
            self.assertListEqual(
                cm.output, [f"ERROR:src.tasks.services.tasks_service:{expected}",]
            )

        total_calls = (
            self.tasks_service.task_manager.get_tasks_assigned_to_and_scheduled_between.call_count
        )
        self.assertEqual(total_calls, 2)

    def test_send_today_tasks_notifications(self):
        self.tasks_service.task_manager.all_assigned_to_for_scheduled_between = (
            MagicMock(return_value=["assigned_123"])
        )
        self.tasks_service.notify_tasks_to_assigned = MagicMock()

        result = self.tasks_service.send_today_tasks_notifications()

        self.assertEqual(result, 1)

        (
            self.tasks_service.task_manager.all_assigned_to_for_scheduled_between.assert_called_once()
        )
        self.tasks_service.notify_tasks_to_assigned.assert_called_once()
