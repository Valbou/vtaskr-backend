from unittest import TestCase

from vtasks.sqlalchemy.database import SQLService, DBType


class DBTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.sql_test = SQLService(DBType.TEST)


class FlaskTestCase(TestCase):
    pass
