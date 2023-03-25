from unittest import TestCase

from redis import Redis

from vtasks.redis.database import NoSQLService, NoSQLSession


class TestNoSQLService(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.nosql_test = NoSQLService(testing=True)
        self.nosql_prod = NoSQLService(testing=False)

    def test_db_test_not_equal_to_prod(self):
        self.assertNotEqual(
            self.nosql_test.get_database_url(), self.nosql_prod.get_database_url()
        )
        self.assertTrue(self.nosql_test.get_database_url().startswith("redis://"))
        self.assertTrue(self.nosql_prod.get_database_url().startswith("redis://"))

    def test_get_engine(self):
        self.assertIsInstance(self.nosql_test.get_engine(), Redis)

    def test_get_session(self):
        self.assertIsInstance(self.nosql_test.get_session(), NoSQLSession)

    def test_db_connection(self):
        r = self.nosql_test.get_engine()
        self.assertTrue(r.ping())
        self.assertTrue(r.set("test", "testing", ex=1))
        self.assertEqual(r.get("test").decode(), "testing")
