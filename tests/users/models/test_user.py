from unittest import TestCase
from datetime import datetime
from typing import Union

from faker import Faker

from vtasks.users import User


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
        self.assertEqual(User.__annotations__.get("id"), str)
        self.assertEqual(User.__annotations__.get("first_name"), str)
        self.assertEqual(User.__annotations__.get("last_name"), str)
        self.assertEqual(User.__annotations__.get("email"), str)
        self.assertEqual(User.__annotations__.get("hash_password"), str)
        self.assertEqual(User.__annotations__.get("locale"), str)
        self.assertEqual(User.__annotations__.get("created_at"), datetime)
        self.assertEqual(
            User.__annotations__.get("last_login_at"), Union[datetime, None]
        )

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

    def test_from_external_data(self):
        previous_hash = self.user.hash_password
        data = {
            "id": "new_id",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@valbou.fr",
            "created_at": "created_at",
            "last_login_at": "last_login_at",
            "password": "passwordA1#",
            "hash_password": "hash_password",
            "other": "other",
        }
        self.user.from_external_data(data)
        self.assertNotEqual(self.user.id, "new_id")
        self.assertEqual(self.user.first_name, "first_name")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.email, "email@valbou.fr")
        self.assertNotEqual(str(self.user.created_at), "created_at")
        self.assertNotEqual(str(self.user.last_login_at), "last_login_at")
        self.assertNotEqual(self.user.hash_password, "passwordA1#")
        self.assertTrue(self.user.check_password("passwordA1#"))
        self.assertNotEqual(self.user.hash_password, "hash_password")
        self.assertNotEqual(self.user.hash_password, previous_hash)

    def test_to_external_data(self):
        data = self.user.to_external_data()
        self.assertEqual(data.pop("id"), self.user.id)
        self.assertEqual(data.pop("first_name"), self.user.first_name)
        self.assertEqual(data.pop("last_name"), self.user.last_name)
        self.assertEqual(data.pop("email"), self.user.email)
        self.assertEqual(data.pop("created_at"), str(self.user.created_at))
        self.assertEqual(data.pop("last_login_at"), str(self.user.last_login_at))
        self.assertIsNone(data.pop("password", None))
        self.assertIsNone(data.pop("hash_password", None))
        self.assertEqual(len(data), 0)
