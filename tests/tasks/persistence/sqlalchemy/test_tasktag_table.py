from tests import BaseTestCase

from vtasks.tasks.persistence import TaskDB, TagDB
from vtasks.tasks import Task, Tag


class TestTaskTagTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "taskstags"
        self.columns_name = [
            "tag_id",
            "task_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestTaskTagAssociation(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.tag_db = TagDB()
        self.task_db = TaskDB()

    def _create_tag(self) -> Tag:
        tag = Tag(
            user_id=self.user.id,
            title=self.fake.text(max_nb_chars=50),
        )
        return tag

    def _create_task(self) -> Task:
        task = Task(
            user_id=self.user.id,
            title=self.fake.sentence(),
        )
        return task

    def test_add_tag_to_a_task(self):
        with self.app.sql_service.get_session() as session:
            tag_1 = self._create_tag()
            tag_2 = self._create_tag()
            task = self._create_task()
            self.task_db.save(session, task)
            task.tags.append(tag_1)
            task.tags.append(tag_2)
            session.commit()
            task_id = task.id

        with self.app.sql_service.get_session() as session:
            saved_task = self.task_db.load(session, task_id)
            self.assertEqual(len(saved_task.tags), 2)

    def test_add_task_to_a_tag(self):
        with self.app.sql_service.get_session() as session:
            task_1 = self._create_task()
            task_2 = self._create_task()
            tag = self._create_tag()
            self.tag_db.save(session, tag)
            tag.tasks.append(task_1)
            tag.tasks.append(task_2)
            session.commit()
            tag_id = tag.id

        with self.app.sql_service.get_session() as session:
            saved_tag = self.tag_db.load(session, tag_id)
            self.assertEqual(len(saved_tag.tasks), 2)
