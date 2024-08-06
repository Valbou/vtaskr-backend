from unittest.mock import MagicMock

from src.settings import LOCALE, TIMEZONE
from src.users.managers import UserManager
from src.users.models import User
from tests.base_test import DummyBaseTestCase


class TestUserManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_m = UserManager(services=self.app.dependencies)

    def _get_user(self) -> User:
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        user.set_password(self.generate_password())
        return user

    def test_create_user(self):
        self.user_m.user_db.save = MagicMock()

        user = self.user_m.create_user(
            session=None,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            password=self.generate_password(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )

        self.user_m.user_db.save.assert_called_once()

        self.assertIsInstance(user, User)

    def test_get_user(self):
        base_user = self._get_user()
        self.user_m.user_db.load = MagicMock(return_value=base_user)

        user = self.user_m.get_user(session=None, user_id="user_132")

        self.user_m.user_db.load.assert_called_once()
        self.assertEqual(base_user.id, user.id)

    def test_update_user(self):
        user = self._get_user()
        self.user_m.user_db.save = MagicMock()

        result = self.user_m.update_user(session=None, user=user)

        self.user_m.user_db.save.assert_called_once()
        self.assertTrue(result)

    def test_delete_user(self):
        user = self._get_user()
        self.user_m.user_db.delete = MagicMock()

        result = self.user_m.delete_user(session=None, user=user)

        self.user_m.user_db.delete.assert_called_once()
        self.assertTrue(result)

    def test_find_user_by_email(self):
        self.user_m.user_db.find_user_by_email = MagicMock()

        self.user_m.find_user_by_email(session=None, email="test@example.com")

        self.user_m.user_db.find_user_by_email.assert_called_once()

    def test_clean_users(self):
        self.user_m.user_db.clean_unused = MagicMock()

        self.user_m.clean_users()

        self.user_m.user_db.clean_unused.assert_called_once()
