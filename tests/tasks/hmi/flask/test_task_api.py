from datetime import datetime

from pytz import utc

from tests.base_test import BaseTestCase
from src.tasks.models import Task
from src.tasks.persistence import TaskDB

URL_API = "/api/v1"


class TestTaskAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.task_db = TaskDB()

    def test_get_task_no_login(self):
        self.create_user()
        task = Task(tenant_id=self.group.id, title=self.fake.sentence(nb_words=8))
        with self.app.sql.get_session() as session:
            self.task_db.save(session, task)

            response = self.client.get(
                f"{URL_API}/task/{task.id}", headers=self.headers
            )
            self.assertEqual(response.status_code, 401)

    def test_get_task(self):
        headers = self.get_token_headers()
        task = Task(tenant_id=self.group.id, title=self.fake.sentence(nb_words=8))
        with self.app.sql.get_session() as session:
            self.task_db.save(session, task)

            response = self.client.get(f"{URL_API}/task/{task.id}", headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_update_task_put(self):
        headers = self.get_token_headers()
        task = Task(tenant_id=self.group.id, title=self.fake.sentence(nb_words=8))
        with self.app.sql.get_session() as session:
            self.task_db.save(session, task)

            new_title = self.fake.sentence(nb_words=5)
            done_at = datetime.now(utc).isoformat()
            data = {
                "title": new_title,
                "done": done_at,
            }

            response = self.client.put(
                f"{URL_API}/task/{task.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(task.title, new_title)
            self.assertEqual(response.json.get("title"), new_title)
            done = datetime.fromisoformat(done_at)
            result_done = datetime.fromisoformat(response.json.get("done"))
            self.assertEqual(result_done, done)
            self.assertFalse(response.json.get("emergency"))

    def test_update_task_patch(self):
        headers = self.get_token_headers()
        task = Task(tenant_id=self.group.id, title=self.fake.sentence(nb_words=8))
        with self.app.sql.get_session() as session:
            self.task_db.save(session, task)

            new_title = self.fake.sentence(nb_words=5)
            data = {
                "title": new_title,
                "emergency": True,
            }

            response = self.client.patch(
                f"{URL_API}/task/{task.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(task.title, new_title)
            self.assertEqual(response.json.get("title"), new_title)
            self.assertTrue(response.json.get("emergency"))
            self.assertFalse(response.json.get("important"))

    def test_delete_task(self):
        headers = self.get_token_headers()
        task = Task(tenant_id=self.group.id, title=self.fake.sentence(nb_words=8))
        with self.app.sql.get_session() as session:
            self.task_db.save(session, task)

            response = self.client.delete(f"{URL_API}/task/{task.id}", headers=headers)
            self.assertEqual(response.status_code, 204)
