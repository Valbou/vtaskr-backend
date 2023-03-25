from tests import BaseTestCase
from tests.utils.db_utils import text_query_table_exists

from vtasks.users.models import User
from vtasks.users.persistence import UserDB


class TestUserTable(BaseTestCase):
    def test_users_table_exists(self):
        with self.app.sql_service.get_session() as session:
            result = session.execute(
                text_query_table_exists(), params={"table": "users"}
            ).scalar_one_or_none()
            self.assertTrue(result)


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
        with self.app.sql_service.get_session() as session:
            self.assertIsNone(self.user_db.load(session, self.user.id))
            self.assertTrue(self.user_db.save(session, self.user))
            self.assertTrue(self.user_db.exists(session, self.user.id))
            old_first_name = self.user.first_name
            self.user.first_name = "abc"
            session.commit()
            user = self.user_db.load(session, self.user.id)
            self.assertNotEqual(old_first_name, user.first_name)
            self.assertEqual(user.id, self.user.id)
            self.assertTrue(self.user_db.delete(session, self.user))
            self.assertFalse(self.user_db.exists(session, self.user.id))

    def test_user_find_login(self):
        with self.app.sql_service.get_session() as session:
            self.assertTrue(self.user_db.save(session, self.user))
            user = self.user_db.find_login(session, email=self.user.email)
            self.assertEqual(user.first_name, self.user.first_name)
