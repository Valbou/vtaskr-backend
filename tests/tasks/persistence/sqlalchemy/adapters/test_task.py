from tests import BaseTestCase
from vtaskr.tasks import Tag, Task
from vtaskr.tasks.persistence import TagDB, TaskDB


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

    def test_add_new_tag(self):
        tag_1 = Tag(self.user.id, self.fake.sentence(nb_words=2)[:50])
        tag_2 = Tag(self.user.id, self.fake.sentence(nb_words=2)[:50])
        with self.app.sql.get_session() as session:
            self.task.add_tags([tag_1, tag_2])
            self.task_db.save(session, self.task)

            tag_db = TagDB()
            self.assertTrue(tag_db.exists(session, tag_1.id))
            self.assertTrue(tag_db.exists(session, tag_2.id))
