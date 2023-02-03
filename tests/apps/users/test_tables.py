from sqlalchemy.orm import Session

from faker import Faker

from tests.db_utils import text_query_table_exists
from tests.base_test import DBTestCase

from src.vtasks.apps.users.models import User
from src.vtasks.apps.users.persistence import UserDB
from src.vtasks.database import DBType


class TestUserTable(DBTestCase):
    def test_users_table_exists(self):
        with Session(self.sql_test.get_engine()) as session:
            result = session.execute(
                text_query_table_exists(), params={"table": "users"}
            ).scalar_one_or_none()
            self.assertTrue(result)


class TestUserAdapter(DBTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user_db = UserDB(DBType.TEST)
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
            hash_password=self.fake.password(),
        )

    def test_insert_user_and_reload_it(self):
        with self.user_db.get_session() as session:
            self.assertTrue(self.user_db.save(session, self.user))
            user = self.user_db.load(session, self.user.id)
            self.assertEqual(user.id, self.user.id)

    def test_insert_user_and_delete_it(self):
        with self.user_db.get_session() as session:
            self.assertTrue(self.user_db.save(session, self.user))
            user = self.user_db.load(session, self.user.id)
            self.assertEqual(user.id, self.user.id)
            self.assertTrue(self.user_db.delete(session, self.user))
            self.assertIsNone(self.user_db.load(session, self.user.id))

    def test_user_exists(self):
        with self.user_db.get_session() as session:
            self.assertTrue(self.user_db.save(session, self.user))
            self.assertTrue(self.user_db.exists(session, self.user.id))
            self.assertTrue(self.user_db.delete(session, self.user))
            self.assertFalse(self.user_db.exists(session, self.user.id))
