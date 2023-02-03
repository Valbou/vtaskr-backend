from sqlalchemy.orm import Session

from faker import Faker

from tests.db_utils import text_query_table_exists
from tests.base_test import DBTestCase

from src.vtasks.apps.users.models import User
from src.vtasks.apps.users.persistence import UserDB


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
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
            password=self.fake.password(),
        )

#     def test_insert_user(self):
#         UserDB.save(user)
