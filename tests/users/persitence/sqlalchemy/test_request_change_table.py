from datetime import datetime, timedelta

from tests import BaseTestCase
from vtasks.base.config import REQUEST_DAYS_HISTORY
from vtasks.users.models import RequestChange, RequestType
from vtasks.users.persistence import RequestChangeDB


class TestRequestChangeTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "requestschanges"
        self.columns_name = [
            "id",
            "created_at",
            "request_type",
            "email",
            "code",
            "done",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestRequestChangeAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.request_change_db = RequestChangeDB()
        self.request_change = RequestChange(
            RequestType.EMAIL, email=self.fake.email(domain="valbou.fr")
        )

    def test_complete_crud_request_change(self):
        with self.app.sql.get_session() as session:
            self.assertIsNone(
                self.request_change_db.load(session, self.request_change.id)
            )
            self.request_change_db.save(session, self.request_change)
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )
            old_code = self.request_change.code
            self.request_change.code = "abc"  # nosec
            session.commit()
            request_change = self.request_change_db.load(
                session, self.request_change.id
            )
            self.assertNotEqual(old_code, request_change.code)
            self.assertEqual(request_change.id, self.request_change.id)
            self.request_change_db.delete(session, self.request_change)
            self.assertFalse(
                self.request_change_db.exists(session, self.request_change.id)
            )

    def test_in_history(self):
        with self.app.sql.get_session() as session:
            self.request_change_db.save(session, self.request_change)
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )
            self.request_change_db.clean_history(session)
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )

    def test_not_in_history(self):
        self.request_change.created_at = datetime.now() - timedelta(
            days=REQUEST_DAYS_HISTORY
        )

        with self.app.sql.get_session() as session:
            self.request_change_db.save(session, self.request_change)
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )
            self.request_change_db.clean_history(session)
            self.assertFalse(
                self.request_change_db.exists(session, self.request_change.id)
            )
