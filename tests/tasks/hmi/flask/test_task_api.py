from tests import BaseTestCase
from vtasks.tasks.models import Task
from vtasks.tasks.persistence import TaskDB

URL_API = "/api/v1"


class TestTaskAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.task_db = TaskDB()

    def test_get_task_no_login(self):
        self.create_user()
        task = Task(self.user.id, self.fake.sentence(nb_words=8))
        task_db = TaskDB()
        with self.app.sql.get_session() as session:
            task_db.save(session, task)

            response = self.client.get(
                f"{URL_API}/task/{task.id}", headers=self.headers
            )
            self.assertEqual(response.status_code, 401)

    def test_get_task(self):
        headers = self.get_token_headers()
        task = Task(self.user.id, self.fake.sentence(nb_words=8))
        task_db = TaskDB()
        with self.app.sql.get_session() as session:
            task_db.save(session, task)

            response = self.client.get(
                f"{URL_API}/task/{task.id}", headers=headers
            )
            self.assertEqual(response.status_code, 200)
