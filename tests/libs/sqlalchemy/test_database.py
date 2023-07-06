from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from tests.utils.db_utils import check_connection_query
from vtaskr.libs.sqlalchemy.database import SQLService


class TestSQLService(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.sql_test = SQLService(testing=True)
        self.sql_prod = SQLService(testing=False)

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

    def test_get_engine(self):
        self.assertIsInstance(self.sql_test.get_engine(), Engine)

    def test_get_session(self):
        self.assertIsInstance(self.sql_test.get_session(), Session)

    def test_db_connection(self):
        with Session(self.sql_test.get_engine()) as session:
            result = session.execute(check_connection_query()).scalar_one_or_none()
            self.assertEqual(result, 1)

    def test_create_tables(self):
        with patch(
            "vtaskr.libs.sqlalchemy.base.mapper_registry.metadata.create_all"
        ) as mock:
            self.sql_test.create_tables()
            mock.assert_called_once()

    def test_drop_tables(self):
        with patch("vtaskr.libs.sqlalchemy.base.mapper_registry.metadata.drop_all") as mock:
            self.sql_test.drop_tables()
            mock.assert_called_once()
