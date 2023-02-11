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

    def _create_tag(self, session) -> Tag:
        tag = Tag(
            user_id=self.user.id,
            title=self.fake.text(max_nb_chars=50),
        )
        return tag

    def _create_task(self, session) -> Task:
        task = Task(
            user_id=self.user.id,
            title=self.fake.sentence(),
        )
        return task

    def test_add_tag_to_a_task(self):
        with self.app.sql_service.get_session() as session:
            tag = self._create_tag(session)
            task = self._create_task(session)
            task.tags.append(tag)
            session.commit()

    def test_add_task_to_a_tag(self):
        with self.app.sql_service.get_session() as session:
            task = self._create_task(session)
            tag = self._create_tag(session)
            tag.tasks.append(task)
            session.commit()
