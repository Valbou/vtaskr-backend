from tests import BaseTestCase
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
        self.task = Task(self.user.id, self.fake.text(max_nb_chars=50))
        self.tag_1 = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        self.tag_2 = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        self.task.add_tags([self.tag_1, self.tag_2])
        self.task_db.save(session, self.task)

    def test_task_tags(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            self.create_data(session)

            response = self.client.get(
                f"{URL_API}/task/{self.task.id}/tags", headers=headers
            )
            self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for tag in result:
            with self.subTest(tag.get("id")):
                self.assertIn(tag.get("id"), [self.tag_1.id, self.tag_2.id])
