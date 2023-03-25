from unittest import TestCase
from datetime import datetime, timedelta
from typing import Optional

from faker import Faker

from vtasks.tasks import Task, EisenhowerFlag


class TestTask(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.task = Task(
            user_id="1234abcd",
            title=self.fake.sentence(),
        )

    def test_task_table_fields(self):
        self.assertEqual(Task.__annotations__.get("id"), str)
        self.assertEqual(Task.__annotations__.get("user_id"), str)
        self.assertEqual(Task.__annotations__.get("title"), str)
        self.assertEqual(Task.__annotations__.get("description"), str)
        self.assertEqual(Task.__annotations__.get("emergency"), bool)
        self.assertEqual(Task.__annotations__.get("important"), bool)
        self.assertEqual(Task.__annotations__.get("created_at"), Optional[datetime])
        self.assertEqual(Task.__annotations__.get("scheduled_at"), Optional[datetime])
        self.assertEqual(Task.__annotations__.get("duration"), Optional[timedelta])
        self.assertEqual(Task.__annotations__.get("done"), Optional[datetime])

    def test_is_done(self):
        self.assertFalse(self.task.is_done())
        self.task.done = datetime.now()
        self.assertTrue(self.task.is_done())

    def test_eisenhower_flag(self):
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.DELETE)
        self.task.emergency = True
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.DELEGATE)
        self.task.important = True
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.TODO)
        self.task.emergency = False
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.SCHEDULE)
