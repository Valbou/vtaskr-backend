from tests.base_test import BaseTestCase
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence import TagDB

URL_API = "/api/v1"


class TestTagAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.tag_db = TagDB()

    def test_get_tag_no_login(self):
        self.create_user()
        tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            response = self.client.get(f"{URL_API}/tag/{tag.id}", headers=self.headers)
            self.assertEqual(response.status_code, 401)

    def test_get_tag(self):
        headers = self.get_token_headers()
        tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            response = self.client.get(f"{URL_API}/tag/{tag.id}", headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_update_tag_put(self):
        headers = self.get_token_headers()
        tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            new_title = self.fake.text(max_nb_chars=50)
            background = self.fake.color()
            data = {
                "title": new_title,
                "backgound_color": background,
            }

            response = self.client.put(
                f"{URL_API}/tag/{tag.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(tag.title, new_title)
            self.assertEqual(response.json.get("title"), new_title)
            result_background = response.json.get("backgound_color")
            self.assertEqual(result_background, background)
            result_foreground = response.json.get("text_color")
            self.assertEqual(result_foreground, "#FFFFFF")

    def test_update_tag_patch(self):
        headers = self.get_token_headers()
        tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            new_title = self.fake.text(max_nb_chars=50)
            foreground = self.fake.color()
            data = {
                "title": new_title,
                "text_color": foreground,
            }

            response = self.client.patch(
                f"{URL_API}/tag/{tag.id}", json=data, headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(tag.title, new_title)
            self.assertEqual(response.json.get("title"), new_title)
            result_background = response.json.get("backgound_color")
            self.assertEqual(result_background, "#000000")
            result_foreground = response.json.get("text_color")
            self.assertEqual(result_foreground, foreground)

    def test_delete_tag(self):
        headers = self.get_token_headers()
        tag = Tag(self.user.id, self.fake.text(max_nb_chars=50))
        with self.app.sql.get_session() as session:
            self.tag_db.save(session, tag)

            response = self.client.delete(f"{URL_API}/tag/{tag.id}", headers=headers)
            self.assertEqual(response.status_code, 204)
