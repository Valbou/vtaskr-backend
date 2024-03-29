from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.settings import UNUSED_ACCOUNT_DELAY
from src.users.models import User
from src.users.persistence import UserDB
from tests.base_test import BaseTestCase


class TestUserAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_db = UserDB()
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            hash_password=self.fake.password(),
        )

    def test_complete_crud_user(self):
        with self.app.sql.get_session() as session:
            self.assertIsNone(self.user_db.load(session, self.user.id))
            self.user_db.save(session, self.user)
            self.assertTrue(self.user_db.exists(session, self.user.id))
            old_first_name = self.user.first_name
            self.user.first_name = "abc"
            session.commit()
            user = self.user_db.load(session, self.user.id)
            self.assertNotEqual(old_first_name, user.first_name)
            self.assertEqual(user.id, self.user.id)
            self.user_db.delete(session, self.user)
            self.assertFalse(self.user_db.exists(session, self.user.id))

    def test_user_find_login(self):
        with self.app.sql.get_session() as session:
            self.user_db.save(session, self.user)
            user = self.user_db.find_login(session, email=self.user.email)
            self.assertEqual(user.first_name, self.user.first_name)

    def test_clean_unused_accounts(self):
        old_user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(days=UNUSED_ACCOUNT_DELAY),
        )

        with self.app.sql.get_session() as session:
            self.user_db.save(session, old_user)
            self.user_db.save(session, self.user)
            self.assertTrue(self.user_db.exists(session, self.user.id))
            self.assertTrue(self.user_db.exists(session, old_user.id))

            self.user_db.clean_unused(session)
            self.assertTrue(self.user_db.exists(session, self.user.id))
            self.assertFalse(self.user_db.exists(session, old_user.id))

    def test_not_clean_used_accounts(self):
        old_user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(days=UNUSED_ACCOUNT_DELAY),
            last_login_at=datetime.now(tz=ZoneInfo("UTC")),
        )

        with self.app.sql.get_session() as session:
            self.user_db.save(session, old_user)
            self.assertTrue(self.user_db.exists(session, old_user.id))

            self.user_db.clean_unused(session)
            self.assertTrue(self.user_db.exists(session, old_user.id))
