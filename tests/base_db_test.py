from unittest import TestCase

from faker import Faker

from vtasks.sqlalchemy.database import SQLService, DBType


class DBTestCase(TestCase):
    defined_sql_service: bool = False
    fake = Faker()

    def setUp(self) -> None:
        super().setUp()
        self._define_sql_service()

    def _define_sql_service(self):
        self.sql_test = SQLService(DBType.TEST)
        self.defined_sql_service = True
