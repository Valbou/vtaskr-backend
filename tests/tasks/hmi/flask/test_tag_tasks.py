from tests.base_test import BaseTestCase
from vtaskr.tasks.models import Tag, Task
from vtaskr.tasks.persistence import TagDB, TaskDB

URL_API = "/api/v1"


class TestTagTasksAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.tag_db = TagDB()
        self.task_db = TaskDB()

    def create_data(self, session):
        self.tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        self.task_1 = Task(self.user.id, self.fake.text(max_nb_chars=50))
        self.task_2 = Task(self.user.id, self.fake.text(max_nb_chars=50))
        self.tag.add_tasks([self.task_1, self.task_2])
        self.tag_db.save(session, self.tag)

    def test_tag_tasks(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
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
        with self.app.sql.get_session() as session:
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
