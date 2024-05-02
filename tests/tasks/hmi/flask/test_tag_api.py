from src.tasks.models import Tag
from src.tasks.persistence import TagDBPort
from src.tasks.settings import APP_NAME
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestTagAPI(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.tag_db: TagDBPort = self.app.dependencies.persistence.get_repository(
            APP_NAME, "Tag"
        )

    def test_get_tag_no_login(self):
        self.create_user()
        tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag_db.save(session, tag)
            session.commit()

        response = self.client.get(f"{URL_API}/tag/{tag.id}", headers=self.headers)
        self.assertEqual(response.status_code, 401)

    def test_get_tag(self):
        headers = self.get_token_headers()
        tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag_db.save(session, tag)
            session.commit()

        response = self.client.get(f"{URL_API}/tag/{tag.id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_tag_put(self):
        headers = self.get_token_headers()
        tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag_db.save(session, tag)
            session.commit()

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
        tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag_db.save(session, tag)
            session.commit()

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
        tag = Tag(tenant_id=self.group.id, title=self.fake.text(max_nb_chars=50))
        with self.app.dependencies.persistence.get_session() as session:
            self.tag_db.save(session, tag)
            session.commit()

        response = self.client.delete(f"{URL_API}/tag/{tag.id}", headers=headers)
        self.assertEqual(response.status_code, 204)
