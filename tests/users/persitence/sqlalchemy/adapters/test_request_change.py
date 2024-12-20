from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.settings import REQUEST_DAYS_HISTORY
from src.users.models import RequestChange, RequestType
from src.users.persistence.sqlalchemy import RequestChangeDB
from tests.base_test import BaseTestCase


class TestRequestChangeAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.request_change_db = RequestChangeDB()
        self.request_change = RequestChange(
            RequestType.EMAIL, email=self.fake.email(domain="valbou.fr")
        )

    def test_complete_crud_request_change(self):
        with self.app.dependencies.persistence.get_session() as session:
            self.assertIsNone(
                self.request_change_db.load(session, self.request_change.id)
            )
            self.request_change_db.save(session, self.request_change)
            session.commit()
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )

            old_code = self.request_change.code
            self.request_change.code = "abc"  # nosec
            self.request_change_db.update(session, self.request_change)
            session.commit()

            request_change = self.request_change_db.load(session, self.request_change.id)
            self.assertNotEqual(old_code, request_change.code)
            self.assertEqual(request_change.id, self.request_change.id)
            self.request_change_db.delete(session, self.request_change)
            session.commit()
            self.assertFalse(
                self.request_change_db.exists(session, self.request_change.id)
            )

    def test_in_history(self):
        with self.app.dependencies.persistence.get_session() as session:
            self.request_change_db.save(session, self.request_change)
            session.commit()
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )
            self.request_change_db.clean_history(session)
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )

    def test_not_in_history(self):
        self.request_change.created_at = datetime.now(ZoneInfo("UTC")) - timedelta(
            days=REQUEST_DAYS_HISTORY
            + 1  # To avoid unaccurate hours between winter and summer
        )

        with self.app.dependencies.persistence.get_session() as session:
            self.request_change_db.save(session, self.request_change)
            session.commit()
            self.assertTrue(
                self.request_change_db.exists(session, self.request_change.id)
            )
            self.request_change_db.clean_history(session)
            self.assertFalse(
                self.request_change_db.exists(session, self.request_change.id)
            )
