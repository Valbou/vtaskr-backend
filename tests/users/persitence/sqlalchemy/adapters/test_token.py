from datetime import datetime, timedelta
from hashlib import sha256
from zoneinfo import ZoneInfo

from src.settings import TOKEN_TEMP_VALIDITY, TOKEN_VALIDITY
from src.users.models import Token, User
from src.users.persistence import TokenDB, UserDB
from tests.base_test import BaseTestCase


class TestTokenAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.user_db = UserDB()
        self.token_db = TokenDB()

        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            hash_password=self.fake.password(),
        )

        with self.app.sql.get_session() as session:
            self.user_db.save(session, self.user)
            self.token = Token(user_id=self.user.id)
            self.token.set_token(
                token=sha256(self.fake.password().encode()).hexdigest()
            )

    def test_complete_crud_token(self):
        with self.app.sql.get_session() as session:
            self.assertIsNone(self.token_db.load(session, self.token.id))
            self.token_db.save(session, self.token)
            self.assertTrue(self.token_db.exists(session, self.token.id))
            old_sha_token = self.token.sha_token
            self.token.sha_token = "abc"  # nosec
            session.commit()
            token = self.token_db.load(session, self.token.id)
            self.assertNotEqual(old_sha_token, token.sha_token)
            self.assertEqual(token.id, self.token.id)
            self.token_db.delete(session, self.token)
            self.assertFalse(self.token_db.exists(session, self.token.id))

    def test_activity_update(self):
        with self.app.sql.get_session() as session:
            last_activity = self.token.last_activity_at
            self.token_db.activity_update(session, self.token)
            self.assertLess(last_activity, self.token.last_activity_at)

    def test_clean_expired(self):
        token = Token(
            self.user.id,
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(seconds=TOKEN_VALIDITY),
        )
        with self.app.sql.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertFalse(self.token_db.exists(session, token.id))

    def test_not_clean_expire_soon_not_temp(self):
        token = Token(
            self.user.id,
            temp=False,
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(seconds=TOKEN_TEMP_VALIDITY),
        )
        with self.app.sql.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_not_clean_not_expired_not_temp(self):
        token = Token(
            self.user.id, temp=False, created_at=datetime.now(tz=ZoneInfo("UTC"))
        )
        with self.app.sql.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_not_clean_not_expired_temp(self):
        token = Token(
            self.user.id,
            temp=True,
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(seconds=TOKEN_TEMP_VALIDITY / 2),
        )
        with self.app.sql.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_temp_clean_expired(self):
        token = Token(
            self.user.id,
            temp=True,
            created_at=datetime.now(tz=ZoneInfo("UTC"))
            - timedelta(seconds=TOKEN_TEMP_VALIDITY),
        )
        with self.app.sql.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertFalse(self.token_db.exists(session, token.id))
