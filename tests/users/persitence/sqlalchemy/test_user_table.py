from sqlalchemy.orm import Session

from faker import Faker

from tests.utils.db_utils import text_query_table_exists
from tests.base_db_test import DBTestCase

from vtasks.users.models import User
from vtasks.users.persistence import UserDB
from vtasks.sqlalchemy.database import DBType


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

    def test_complete_crud_user(self):
        with self.user_db.get_session() as session:
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
