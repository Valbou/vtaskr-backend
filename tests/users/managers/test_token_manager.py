from unittest.mock import MagicMock

from src.users.managers import TokenManager
from src.users.models import Token
from tests.base_test import DummyBaseTestCase


class TestTokenManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.token_m = TokenManager(services=self.app.dependencies)

    def _get_token(self):
        return Token(user_id="user_123")

    def test_create_token(self):
        self.token_m.update_token = MagicMock()

        new_token = self.token_m.create_token(session=None, user_id="user_123")

        self.token_m.update_token.assert_called_once()
        self.assertEqual("user_123", new_token.user_id)

    def test_get_token(self):
        base_token = self._get_token()
        self.token_m.token_db.get_token = MagicMock(return_value=base_token)

        token = self.token_m.get_token(session=None, sha_token="sha_123")  # nosec

        self.token_m.token_db.get_token.assert_called_once()
        self.assertEqual(base_token.id, token.id)

    def test_clean_expired(self):
        self.token_m.token_db.clean_expired = MagicMock()

        self.token_m.clean_expired(session=None)

        self.token_m.token_db.clean_expired.assert_called_once()

    def test_update_token(self):
        base_token = self._get_token()
        self.token_m.token_db.save = MagicMock()

        result = self.token_m.update_token(session=None, token=base_token)

        self.token_m.token_db.save.assert_called_once()
        self.assertTrue(result)

    def test_delete_token(self):
        base_token = self._get_token()
        self.token_m.token_db.delete = MagicMock()

        result = self.token_m.delete_token(session=None, token=base_token)

        self.token_m.token_db.delete.assert_called_once()
        self.assertTrue(result)
