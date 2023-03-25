from tests import BaseTestCase

from vtasks.users.models import User
from vtasks.users.persistence import UserDB


class TestUserTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "users"
        self.columns_name = [
            "id",
            "first_name",
            "last_name",
            "email",
            "hash_password",
            "locale",
            "created_at",
            "last_login_at",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestUserAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_db = UserDB()
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
            hash_password=self.fake.password(),
        )

    def test_complete_crud_user(self):
        with self.app.sql.get_session() as session:
            self.assertIsNone(self.user_db.load(session, self.user.id))
            self.user_db.save(session, self.user)
            self.assertTrue(self.user_db.exists(session, self.user.id))
            old_first_name = self.user.first_name
            self.user.first_name = "abc"
            session.commit()
            user = self.user_db.load(session, self.user.id)
            self.assertNotEqual(old_first_name, user.first_name)
            self.assertEqual(user.id, self.user.id)
            self.user_db.delete(session, self.user)
            self.assertFalse(self.user_db.exists(session, self.user.id))

    def test_user_find_login(self):
        with self.app.sql.get_session() as session:
            self.user_db.save(session, self.user)
            user = self.user_db.find_login(session, email=self.user.email)
            self.assertEqual(user.first_name, self.user.first_name)
