from datetime import datetime
from unittest import TestCase

from faker import Faker

from src.users.models import Invitation


class TestInvitation(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.invitation = Invitation(
            from_user_id="user_id",
            to_user_email="you@example.com",
            with_roletype_id="roletype_id",
            in_group_id="group_id",
        )

    def test_table_fields(self):
        self.assertEqual(Invitation.__annotations__.get("id"), str | None)
        self.assertEqual(Invitation.__annotations__.get("created_at"), datetime | None)
        self.assertEqual(Invitation.__annotations__.get("from_user_id"), str)
        self.assertEqual(Invitation.__annotations__.get("to_user_email"), str)
        self.assertEqual(Invitation.__annotations__.get("with_roletype_id"), str)
        self.assertEqual(Invitation.__annotations__.get("in_group_id"), str)
        self.assertEqual(Invitation.__annotations__.get("hash"), str)

    def test_consistency_gen_hash(self):
        self.assertIsInstance(self.invitation.gen_hash(), str)
        self.assertEqual(len(self.invitation.gen_hash()), 128)
        self.assertEqual(self.invitation.gen_hash(), self.invitation.gen_hash())
        self.assertTrue(self.invitation.check_hash(self.invitation.gen_hash()))

        invitation_2 = Invitation(
            from_user_id="user_id",
            to_user_email="you@example.com",
            with_roletype_id="roletype_id",
            in_group_id="group_id",
        )
        self.assertNotEqual(self.invitation.gen_hash(), invitation_2.gen_hash())
        self.assertFalse(self.invitation.check_hash(invitation_2.gen_hash()))
