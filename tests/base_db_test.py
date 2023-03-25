from unittest import TestCase

from vtasks.sqlalchemy.database import SQLService, DBType


class DBTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._define_sql_service()

    def _define_sql_service(self):
        self.sql_test = SQLService(DBType.TEST)
