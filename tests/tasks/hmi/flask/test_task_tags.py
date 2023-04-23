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

    def test_task_set_tags(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            self.create_data(session)
            task = self.task_db.load(session, self.task.id)
            self.assertEqual(len(task.tags), 2)
            previous_ids = [t.id for t in task.tags]

            tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
            self.tag_db.save(session, tag)

            # Check with bad data
            data = {"tags": [123, 465]}
            response = self.client.put(
                f"{URL_API}/task/{self.task.id}/tags/set", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 400)

            # Check with good data
            data = {"tags": [tag.id]}
            response = self.client.put(
                f"{URL_API}/task/{self.task.id}/tags/set", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 201)

        with self.app.sql.get_session() as session:  # required to update task informations
            task = self.task_db.load(session, self.task.id)
            self.assertEqual(len(task.tags), 1)
            self.assertNotIn(task.tags[0].id, previous_ids)

    def test_task_clean_tags(self):
        headers = self.get_token_headers()
        with self.app.sql.get_session() as session:
            self.create_data(session)
            task = self.task_db.load(session, self.task.id)
            self.assertEqual(len(task.tags), 2)

            response = self.client.delete(
                f"{URL_API}/task/{self.task.id}/tags/clean", headers=headers
            )
            self.assertEqual(response.status_code, 204)

        with self.app.sql.get_session() as session:  # required to update task informations
            task = self.task_db.load(session, self.task.id)
            self.assertEqual(len(task.tags), 0)
