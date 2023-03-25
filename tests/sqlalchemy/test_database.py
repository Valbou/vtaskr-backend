from unittest import TestCase

from sqlalchemy.orm import Session

from tests.utils.db_utils import check_connection_query

from vtasks.sqlalchemy.database import SQLService, DBType


class TestSQLService(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.sql_test = SQLService(DBType.TEST)
        self.sql_prod = SQLService(DBType.PROD)

    def test_db_test_not_equal_to_prod(self):
        self.assertNotEqual(
            self.sql_test.get_database_url(), self.sql_prod.get_database_url()
        )
        self.assertTrue(
            self.sql_test.get_database_url().startswith("postgresql+psycopg2://")
        )
        self.assertTrue(
            self.sql_prod.get_database_url().startswith("postgresql+psycopg2://")
        )

    def test_db_connection(self):
        with Session(self.sql_test.get_engine()) as session:
            result = session.execute(check_connection_query()).scalar_one_or_none()
            self.assertEqual(result, 1)
