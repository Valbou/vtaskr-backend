from datetime import datetime, timedelta
from unittest import TestCase
from zoneinfo import ZoneInfo

from faker import Faker

from src.settings import REQUEST_DAYS_HISTORY, REQUEST_VALIDITY
from src.users import RequestChange, RequestType


class TestRequestChange(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()

    def create_request_change(
        self, type: RequestType = RequestType.PASSWORD, email: str | None = None
    ) -> RequestChange:
        email = email or self.fake.email(domain="valbou.fr")
        return RequestChange(type, email)

    def test_request_change_table_fields(self):
        self.assertEqual(RequestChange.__annotations__.get("id"), str | None)
        self.assertEqual(
            RequestChange.__annotations__.get("created_at"), datetime | None
        )
        self.assertEqual(RequestChange.__annotations__.get("request_type"), RequestType)
        self.assertEqual(RequestChange.__annotations__.get("email"), str)
        self.assertEqual(RequestChange.__annotations__.get("code"), str | None)
        self.assertEqual(RequestChange.__annotations__.get("done"), bool)

    def test_request_change_is_valid(self):
        request_change = self.create_request_change()
        self.assertTrue(request_change.is_valid())

    def test_request_change_invalid_if_done(self):
        request_change = self.create_request_change()
        request_change.done = True
        self.assertFalse(request_change.is_valid())

    def test_request_change_old_invalid(self):
        request_change = self.create_request_change()
        request_change.created_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            seconds=REQUEST_VALIDITY
        )
        self.assertFalse(request_change.is_valid())

    def test_request_change_in_history(self):
        request_change = self.create_request_change()
        request_change.created_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            seconds=REQUEST_VALIDITY
        )
        self.assertFalse(
            request_change.created_at < RequestChange.history_expired_before()
        )

    def test_request_change_out_of_history(self):
        request_change = self.create_request_change()
        request_change.created_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            days=REQUEST_DAYS_HISTORY
        )
        self.assertTrue(
            request_change.created_at < RequestChange.history_expired_before()
        )

    def test_valid_after(self):
        request_change = self.create_request_change()
        self.assertTrue(request_change.created_at > RequestChange.valid_after())

    def test_invalid_after(self):
        request_change = self.create_request_change()
        request_change.created_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            seconds=REQUEST_VALIDITY
        )
        self.assertFalse(request_change.created_at > RequestChange.valid_after())

    def test_check_code(self):
        request_change = self.create_request_change()
        self.assertIsInstance(request_change.code, str)
        self.assertTrue(request_change.check_code(request_change.code))
        self.assertFalse(request_change.check_code(self.fake.bothify("###???")))

    def test_consistency_gen_hash(self):
        request_change = self.create_request_change()
        self.assertIsInstance(request_change.gen_hash(), str)
        self.assertEqual(len(request_change.gen_hash()), 64)
        self.assertEqual(request_change.gen_hash(), request_change.gen_hash())
        self.assertTrue(request_change.check_hash(request_change.gen_hash()))

        request_change_2 = self.create_request_change()
        self.assertNotEqual(request_change.gen_hash(), request_change_2.gen_hash())
        self.assertFalse(request_change.check_hash(request_change_2.gen_hash()))

    def test_set_email(self):
        request_change = self.create_request_change()
        email = request_change.email
        self.assertTrue(request_change.set_email(self.fake.email(domain="valbou.fr")))
        self.assertNotEqual(email, request_change.email)
        self.assertFalse(request_change.set_email(self.fake.word()))

    def test_mark_as_done(self):
        request_change = self.create_request_change()
        self.assertFalse(request_change.done)
        request_change.mark_as_done()
        self.assertTrue(request_change.done)
