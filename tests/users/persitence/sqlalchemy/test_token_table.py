from datetime import datetime, timedelta

from hashlib import sha256

from tests import BaseTestCase

from vtasks.base.config import TOKEN_VALIDITY, TOKEN_TEMP_VALIDITY
from vtasks.users.models import User, Token
from vtasks.users.persistence import UserDB, TokenDB


class TestTokenTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "tokens"
        self.columns_name = [
            "id",
            "created_at",
            "last_activity_at",
            "temp",
            "temp_code",
            "sha_token",
            "user_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)


class TestTokenAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.user_db = UserDB()
        self.token_db = TokenDB()

        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
            hash_password=self.fake.password(),
        )

        with self.app.sql_service.get_session() as session:
            self.user_db.save(session, self.user)
            self.token = Token(
                token=sha256(self.fake.password().encode()).hexdigest(),
                user_id=self.user.id,
            )

    def test_complete_crud_token(self):
        with self.app.sql_service.get_session() as session:
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
        with self.app.sql_service.get_session() as session:
            last_activity = self.token.last_activity_at
            self.token_db.activity_update(session, self.token)
            self.assertLess(last_activity, self.token.last_activity_at)

    def test_clean_expired(self):
        token = Token(
            self.user.id,
            created_at=datetime.now() - timedelta(seconds=TOKEN_VALIDITY),
        )
        with self.app.sql_service.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertFalse(self.token_db.exists(session, token.id))

    def test_not_clean_expire_soon_not_temp(self):
        token = Token(
            self.user.id,
            temp=False,
            created_at=datetime.now() - timedelta(seconds=TOKEN_TEMP_VALIDITY),
        )
        with self.app.sql_service.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_not_clean_not_expired_not_temp(self):
        token = Token(self.user.id, temp=False, created_at=datetime.now())
        with self.app.sql_service.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_not_clean_not_expired_temp(self):
        token = Token(
            self.user.id,
            temp=True,
            created_at=datetime.now() - timedelta(seconds=TOKEN_TEMP_VALIDITY / 2),
        )
        with self.app.sql_service.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertTrue(self.token_db.exists(session, token.id))

    def test_temp_clean_expired(self):
        token = Token(
            self.user.id,
            temp=True,
            created_at=datetime.now() - timedelta(seconds=TOKEN_TEMP_VALIDITY),
        )
        with self.app.sql_service.get_session() as session:
            self.token_db.save(session, token)
            self.assertTrue(self.token_db.exists(session, token.id))
            self.token_db.clean_expired(session)
            self.assertFalse(self.token_db.exists(session, token.id))
