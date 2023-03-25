from .base_db_test import DBTestCase
from .base_http_test import FlaskTestCase


class BaseTestCase(FlaskTestCase, DBTestCase):
    def setUp(self) -> None:
        super().setUp()

        if not self.defined_http_service:
            self._define_client()

        if not self.defined_sql_service:
            self._define_sql_service()
