from datetime import datetime
from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

from tests.db_utils import text_query_table_exists
from tests.base_test import DBTestCase

from src.vtasks.apps.users import User


class CheckTableUser(DBTestCase):
    def test_users_table_exists(self):
        with Session(self.sql_test.get_engine()) as session:
            result = session.execute(
                text_query_table_exists(), params={"table": "users"}
            ).scalar_one_or_none()
            self.assertTrue(result)

    def test_user_table_fields(self):
        self.assertEqual(User.__annotations__.get("id"), Mapped[str])
        self.assertEqual(User.__annotations__.get("first_name"), Mapped[str])
        self.assertEqual(User.__annotations__.get("last_name"), Mapped[str])
        self.assertEqual(User.__annotations__.get("email"), Mapped[str])
        self.assertEqual(User.__annotations__.get("password"), Mapped[str])
        self.assertEqual(User.__annotations__.get("created_at"), Mapped[datetime])
        self.assertEqual(
            User.__annotations__.get("last_login_at"), Mapped[Union[datetime, None]]
        )
