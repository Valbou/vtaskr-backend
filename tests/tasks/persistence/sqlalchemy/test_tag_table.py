from tests import BaseTestCase

from vtasks.tasks.persistence import TagDB
from vtasks.tasks import Tag


class TestTagTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "tags"
        self.columns_name = [
            "id",
            "created_at",
            "user_id",
            "title",
            "color",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestTagAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.tag_db = TagDB()
        self.tag = Tag(
            user_id=self.user.id,
            title=self.fake.text(max_nb_chars=50),
        )

    def test_complete_crud_tag(self):
        with self.app.sql_service.get_session() as session:
            self.assertIsNone(self.tag_db.load(session, self.tag.id))
            self.assertTrue(self.tag_db.save(session, self.tag))
            self.assertTrue(self.tag_db.exists(session, self.tag.id))
            old_title = self.tag.title
            self.tag.title = "abc"
            session.commit()
            tag = self.tag_db.load(session, self.tag.id)
            self.assertNotEqual(old_title, tag.title)
            self.assertEqual(tag.id, self.tag.id)
            self.assertTrue(self.tag_db.delete(session, self.tag))
            self.assertFalse(self.tag_db.exists(session, self.tag.id))
