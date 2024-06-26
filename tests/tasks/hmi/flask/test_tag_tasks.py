from src.tasks.models import Tag, Task
from src.tasks.persistence import TagDBPort, TaskDBPort
from src.tasks.settings import APP_NAME
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestTagTasksAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.tag_db: TagDBPort = self.app.dependencies.persistence.get_repository(
            APP_NAME, "Tag"
        )
        self.task_db: TaskDBPort = self.app.dependencies.persistence.get_repository(
            APP_NAME, "Task"
        )

    def create_data(self, session):
        self.tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        self.task_1 = Task(
            tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50)
        )
        self.task_2 = Task(
            tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50)
        )
        self.tag.add_tasks([self.task_1, self.task_2])
        self.tag_db.save(session, self.tag)
        session.commit()

    def test_tag_tasks(self):
        headers = self.get_token_headers()
        with self.app.dependencies.persistence.get_session() as session:
            self.create_data(session)

            response = self.client.get(
                f"{URL_API}/tag/{self.tag.id}/tasks", headers=headers
            )
            self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for task in result:
            with self.subTest(task.get("id")):
                self.assertIn(task.get("id"), [self.task_1.id, self.task_2.id])

    def test_tag_tasks_with_filter(self):
        headers = self.get_token_headers()
        with self.app.dependencies.persistence.get_session() as session:
            self.create_data(session)

            response = self.client.get(
                f"{URL_API}/tag/{self.tag.id}/tasks?limit=1", headers=headers
            )
            self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        for task in result:
            with self.subTest(task.get("id")):
                self.assertIn(task.get("id"), [self.task_1.id, self.task_2.id])
