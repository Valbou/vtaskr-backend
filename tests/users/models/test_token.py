from datetime import datetime, timedelta
from unittest import TestCase
from zoneinfo import ZoneInfo

from faker import Faker

from src.libs.security.utils import get_id
from src.settings import TOKEN_TEMP_VALIDITY, TOKEN_VALIDITY
from src.users import Token


class TestToken(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()

    def create_token(self, temp: bool = True):
        return Token(user_id=get_id(), temp=temp)

    def test_table_fields(self):
        self.assertEqual(Token.__annotations__.get("id"), str | None)
        self.assertEqual(Token.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(Token.__annotations__.get("last_activity_at"), datetime | None)
        self.assertEqual(Token.__annotations__.get("temp"), bool)
        self.assertEqual(Token.__annotations__.get("temp_code"), str | None)
        self.assertEqual(Token.__annotations__.get("sha_token"), str | None)
        self.assertEqual(Token.__annotations__.get("user_id"), str)

    def test_token_is_valid(self):
        token = self.create_token(temp=False)
        self.assertTrue(token.is_valid())

    def test_token_old_invalid(self):
        token = self.create_token(temp=False)
        token.last_activity_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            seconds=TOKEN_VALIDITY
        )
        self.assertFalse(token.is_valid())

    def test_token_temp_is_invalid(self):
        token = self.create_token()
        self.assertFalse(token.is_valid())

    def test_token_temp_is_temp_valid(self):
        token = self.create_token()
        self.assertTrue(token.is_temp_valid())

    def test_token_old_temp_is_temp_invalid(self):
        token = self.create_token()
        token.created_at = datetime.now(tz=ZoneInfo("UTC")) - timedelta(
            seconds=TOKEN_TEMP_VALIDITY
        )
        self.assertFalse(token.is_temp_valid())

    def test_token_not_temp_is_temp_invalid(self):
        token = self.create_token(temp=False)
        self.assertFalse(token.is_temp_valid())

    def test_validate_token(self):
        token = self.create_token()
        self.assertFalse(token.validate_token(self.fake.password()))
        self.assertTrue(token.validate_token(token.temp_code))

    def test_token_to_string(self):
        token = self.create_token(temp=False)
        self.assertEqual(str(token), f"Token {token.sha_token}")

    def test_token_to_representation(self):
        token = self.create_token(temp=False)
        self.assertEqual(repr(token), f"<Token {token.sha_token!r}>")

    def test_token_id_unicity(self):
        token1 = self.create_token()
        token2 = self.create_token()
        self.assertNotEqual(token1.id, token2.id)
