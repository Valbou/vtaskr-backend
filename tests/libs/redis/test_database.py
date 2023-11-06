from unittest import TestCase

from redis import Redis

from src.libs.redis.database import NoSQLService, NoSQLSession, TestNoSQLService


class TestFakeNoSQLService(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.nosql_test = TestNoSQLService()
        self.nosql_prod = NoSQLService()

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

    def test_pipe_session(self):
        with self.nosql_test.get_session() as pipe:
            pipe.set("one", 1, ex=1)
            pipe.set("two", 2, ex=1)
            pipe.set("three", 3, ex=1)

        r = self.nosql_test.get_engine()
        self.assertEqual(r.get("one"), b"1")
        self.assertEqual(r.get("two"), b"2")
        self.assertEqual(r.get("three"), b"3")
        self.assertIsNone(r.get("four"))
