from datetime import datetime, timedelta
from typing import Optional
from unittest import TestCase

from faker import Faker
from pytz import utc

from vtaskr.tasks import EisenhowerFlag, Tag, Task


class TestTask(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.tenant_id = "1234abcd"
        self.task = Task(
            tenant_id=self.tenant_id,
            title=self.fake.sentence(),
        )

    def test_task_table_fields(self):
        self.assertEqual(Task.__annotations__.get("id"), str)
        self.assertEqual(Task.__annotations__.get("tenant_id"), str)
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
        self.task.done = datetime.now(utc)
        self.assertTrue(self.task.is_done())

    def test_eisenhower_flag(self):
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.DELETE)
        self.task.emergency = True
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.DELEGATE)
        self.task.important = True
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.DO)
        self.task.emergency = False
        self.assertEqual(self.task.get_eisenhower_flag(), EisenhowerFlag.SCHEDULE)

    def test_add_and_remove_tags(self):
        tag_1 = Tag(self.tenant_id, self.fake.text(max_nb_chars=50))
        tag_2 = Tag(self.tenant_id, self.fake.text(max_nb_chars=50))
        self.task.add_tags([tag_1, tag_2])
        self.assertEqual(len(self.task.tags), 2)

        self.task.remove_tags([tag_2.id])
        self.assertEqual(len(self.task.tags), 1)
        self.assertEqual(self.task.tags[0].id, tag_1.id)
