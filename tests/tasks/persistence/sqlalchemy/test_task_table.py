from vtasks.tasks import Task
from vtasks.tasks.persistence import TaskDB

from tests import BaseTestCase


class TestTaskTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "tasks"
        self.columns_name = [
            "id",
            "created_at",
            "user_id",
            "title",
            "description",
            "emergency",
            "important",
            "scheduled_at",
            "duration",
            "done",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestTaskAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.task_db = TaskDB()
        self.task = Task(
            user_id=self.user.id,
            title=self.fake.sentence(),
        )

    def test_complete_crud_task(self):
        with self.app.sql.get_session() as session:
            self.assertIsNone(self.task_db.load(session, self.task.id))
            self.task_db.save(session, self.task)
            self.assertTrue(self.task_db.exists(session, self.task.id))
            old_title = self.task.title
            self.task.title = "abc"
            session.commit()
            task = self.task_db.load(session, self.task.id)
            self.assertNotEqual(old_title, task.title)
            self.assertEqual(task.id, self.task.id)
            self.task_db.delete(session, self.task)
            self.assertFalse(self.task_db.exists(session, self.task.id))
