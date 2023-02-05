from hashlib import sha256

from tests import BaseTestCase
from tests.utils.db_utils import text_query_table_exists

from vtasks.users.models import User, Token
from vtasks.users.persistence import UserDB, TokenDB


class TestTokenTable(BaseTestCase):
    def test_tokens_table_exists(self):
        with self.app.sql_service.get_session() as session:
            result = session.execute(
                text_query_table_exists(), params={"table": "tokens"}
            ).scalar_one_or_none()
            self.assertTrue(result)


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
            self.assertTrue(self.token_db.save(session, self.token))
            self.assertTrue(self.token_db.exists(session, self.token.id))
            old_sha_token = self.token.sha_token
            self.token.sha_token = "abc"  # nosec
            session.commit()
            token = self.token_db.load(session, self.token.id)
            self.assertNotEqual(old_sha_token, token.sha_token)
            self.assertEqual(token.id, self.token.id)
            self.assertTrue(self.token_db.delete(session, self.token))
            self.assertFalse(self.token_db.exists(session, self.token.id))
