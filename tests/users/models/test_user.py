from datetime import datetime
from unittest import TestCase
from zoneinfo import ZoneInfo

from babel import Locale
from faker import Faker

from src.settings import UNUSED_ACCOUNT_DELAY
from src.users import User


class TestUser(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.user = User(  # nosec
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
            hash_password="1234",
        )

    def test_user_table_fields(self):
        self.assertEqual(User.__annotations__.get("id"), str | None)
        self.assertEqual(User.__annotations__.get("first_name"), str)
        self.assertEqual(User.__annotations__.get("last_name"), str)
        self.assertEqual(User.__annotations__.get("email"), str)
        self.assertEqual(User.__annotations__.get("hash_password"), str | None)
        self.assertEqual(User.__annotations__.get("locale"), Locale | None)
        self.assertEqual(User.__annotations__.get("timezone"), str | None)
        self.assertEqual(User.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(User.__annotations__.get("last_login_at"), datetime | None)

    def test_user_property_fullname(self):
        self.assertEqual(
            f"{self.user.first_name} {self.user.last_name}", self.user.full_name
        )

    def test_user_set_password(self):
        password = "aB#1234aB#1234"  # nosec
        self.user.set_password(password)
        self.assertNotEqual(password, self.user.hash_password)

    def test_user_check_password(self):
        password = "aB#1234aB#1234"  # nosec
        self.user.set_password(password)
        self.assertTrue(self.user.check_password(password))

    def test_user_to_string(self):
        self.assertEqual(str(self.user), self.user.full_name)

    def test_user_to_representation(self):
        self.assertEqual(repr(self.user), f"<User {self.user.full_name!r}>")

    def test_user_id_unicity(self):
        user = User(  # nosec
            first_name="A",
            last_name="B",
            email=self.fake.email(domain="valbou.fr"),
            hash_password="azerty",
        )

        self.assertNotEqual(user.id, self.user.id)

    def test_user_unused_date(self):
        unused_limit = User.unused_before()
        delta = datetime.now(tz=ZoneInfo("UTC")) - unused_limit
        self.assertEqual(delta.days, UNUSED_ACCOUNT_DELAY)
