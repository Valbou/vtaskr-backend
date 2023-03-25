from tests import BaseTestCase

from vtasks.tasks.persistence import TaskDB, TagDB, TaskTagDB
from vtasks.tasks import Task, Tag, TaskTag


class TestTaskTagTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "taskstags"
        self.columns_name = [
            "id",
            "created_at",
            "tag_id",
            "task_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestTaskTag(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()

        self.task_db = TaskDB()
        self.task = Task(
            user_id=self.user.id,
            title=self.fake.sentence(),
        )

        self.tag_db = TagDB()
        self.tag = Tag(
            user_id=self.user.id,
            title=self.fake.text(max_nb_chars=50),
        )

        self.tasktag_db = TaskTagDB()
        self.tasktag = TaskTag(
            task_id=self.task.id,
            tag_id=self.tag.id,
        )

    def test_complete_crud_tasktag(self):
        with self.app.sql_service.get_session() as session:
            self.task_db.save(session, self.task)
            self.tag_db.save(session, self.tag)

            self.assertIsNone(self.tasktag_db.load(session, self.tasktag.id))
            self.assertTrue(self.tasktag_db.save(session, self.tasktag))
            self.assertTrue(self.tasktag_db.exists(session, self.task.id, self.tag.id))
            self.assertTrue(self.tasktag_db.delete(session, self.tasktag))
            self.assertFalse(self.tasktag_db.exists(session, self.task.id, self.tag.id))

            self.task_db.delete(session, self.task)
            self.tag_db.delete(session, self.tag)
