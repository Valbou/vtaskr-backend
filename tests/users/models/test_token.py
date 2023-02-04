from unittest import TestCase
from datetime import datetime
from uuid import uuid4

from faker import Faker

from vtasks.users import Token


class TestToken(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.token = Token(user_id=uuid4().hex)

    def test_token_table_fields(self):
        self.assertEqual(Token.__annotations__.get("id"), str)
        self.assertEqual(Token.__annotations__.get("created_at"), datetime)
        self.assertEqual(Token.__annotations__.get("sha_token"), str)
        self.assertEqual(Token.__annotations__.get("user_id"), str)

    def test_token_to_string(self):
        self.assertEqual(str(self.token), f"Token {self.token.sha_token}")

    def test_token_to_representation(self):
        self.assertEqual(repr(self.token), f"<Token {self.token.sha_token!r}>")

    def test_token_id_unicity(self):
        token = Token(user_id=uuid4().hex)
        self.assertNotEqual(token.id, self.token.id)
