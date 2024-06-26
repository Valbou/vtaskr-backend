from src.tasks import Tag, Task
from src.tasks.persistence.sqlalchemy import TagDB, TaskDB
from tests.base_test import BaseTestCase


class TestTagAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.tag_db = TagDB()
        self.tag = Tag(
            tenant_id=self.user.id,
            title=self.fake.text(max_nb_chars=50),
        )

    def test_complete_crud_tag(self):
        with self.app.dependencies.persistence.get_session() as session:
            self.assertIsNone(self.tag_db.load(session, self.tag.id))
            self.tag_db.save(session, self.tag)
            session.commit()

            self.assertTrue(self.tag_db.exists(session, self.tag.id))
            old_title = self.tag.title
            self.tag.title = "abc"
            session.commit()

            tag = self.tag_db.load(session, self.tag.id)
            self.assertNotEqual(old_title, tag.title)
            self.assertEqual(tag.id, self.tag.id)

            self.tag_db.delete(session, self.tag)
            session.commit()
            self.assertFalse(self.tag_db.exists(session, self.tag.id))

    def test_add_new_task(self):
        task_1 = Task(self.user.id, self.fake.text(max_nb_chars=50))
        task_2 = Task(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag.add_tasks([task_1, task_2])
            self.tag_db.save(session, self.tag)
            session.commit()

        task_db = TaskDB()
        self.assertTrue(task_db.exists(session, task_1.id))
        self.assertTrue(task_db.exists(session, task_2.id))

        tags = self.tag_db.task_tags(
            session,
            [
                self.user.id,
            ],
            task_1.id,
        )
        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].id, self.tag.id)
