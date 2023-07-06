from tests.base_test import BaseTestCase
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence import TagDB

URL_API = "/api/v1"


class TestTagsAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.tag_db = TagDB()

    def test_create_tag_no_login(self):
        tag_data = {"nodata": "nodata"}
        response = self.client.post(
            f"{URL_API}/tags", json=tag_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 401)

    def test_create_tag(self):
        headers = self.get_token_headers()
        title = self.fake.text(max_nb_chars=50)
        tag_data = {
            "title": title,
        }
        response = self.client.post(f"{URL_API}/tags", json=tag_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("title"), title)
        self.assertIsInstance(response.json.get("id"), str)
        with self.app.sql.get_session() as session:
            self.assertTrue(self.tag_db.exists(session, response.json.get("id")))

    def test_get_tags_no_login(self):
        response = self.client.get(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_get_tags(self):
        headers = self.get_token_headers()
        tag = Tag(user_id=self.user.id, title=self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            response = self.client.get(f"{URL_API}/tags", headers=headers)
            self.assertEqual(response.status_code, 200)
            result = response.json
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].get("id"), tag.id)

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/tags", headers=self.headers)
        self.assertEqual(response.status_code, 405)
