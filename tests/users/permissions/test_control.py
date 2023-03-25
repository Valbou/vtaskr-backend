from unittest import TestCase

from faker import Faker

from vtasks.users import PermissionControl, Token, User


class PermissionControlTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.control = PermissionControl()
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email="control." + self.fake.email(domain="valbou.fr"),
        )

    def test_is_owner(self):
        token = Token(user_id=self.user.id)
        self.assertTrue(self.control.is_owner(self.user, token))

    def test_is_not_owner(self):
        token = Token(user_id="1234abcd")
        self.assertFalse(self.control.is_owner(self.user, token))
