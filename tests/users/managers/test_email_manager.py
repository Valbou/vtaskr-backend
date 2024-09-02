from src.users.managers import EmailManager
from src.users.models import Group, Invitation, RequestChange, RequestType, RoleType
from tests.base_test import DummyBaseTestCase


class TestEmailManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.email_manager = EmailManager(services=self.app.dependencies)

    def _common_test(self, context: dict, template: str):
        self.assertIsInstance(context, dict)
        self.assertEqual(context["sender"], "vTaskr <contact@valbou.fr>")
        self.assertEqual(context["template"], template)

    def test_get_register_context(self):
        self.create_user()

        context = self.email_manager.get_register_context(user=self.user)

        self._common_test(context=context, template="emails/register")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn(self.user.first_name, context["content_title"])
        self.assertIn(self.user.first_name, context["subject"])

    def test_get_login_context(self):
        self.create_user()
        code = "code_123"

        context = self.email_manager.get_login_context(user=self.user, code=code)

        self._common_test(context=context, template="emails/login")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("New login", context["subject"])
        self.assertEqual(context["code"], code)

    def test_get_email_change_old_context(self):
        self.create_user()
        request = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )

        context = self.email_manager.get_email_change_old_context(
            user=self.user, request_change=request
        )

        self._common_test(context=context, template="emails/change_email")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("Change your Email", context["subject"])
        self.assertEqual(context["code"], request.code)

    def test_get_email_change_new_context(self):
        self.create_user()
        request = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )
        sec_hash = request.gen_hash()

        context = self.email_manager.get_email_change_new_context(
            user=self.user, new_email=request.email, sec_hash=sec_hash
        )

        self._common_test(context=context, template="emails/change_email")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("Change your Email", context["subject"])
        self.assertIn(
            f"hash={sec_hash}&email={request.email}", context["call_to_action_link"]
        )

    def test_get_password_change_context(self):
        self.create_user()
        request = RequestChange(
            request_type=RequestType.PASSWORD, email="test@example.com"
        )
        sec_hash = request.gen_hash()

        context = self.email_manager.get_password_change_context(
            user=self.user, sec_hash=sec_hash
        )

        self._common_test(context=context, template="emails/change_password")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("Password Change", context["subject"])
        self.assertIn(
            f"hash={sec_hash}&email={self.user.email}", context["call_to_action_link"]
        )

    def test_get_delete_context(self):
        self.create_user()

        context = self.email_manager.get_delete_context(user=self.user)

        self._common_test(context=context, template="emails/delete")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("Account deleted", context["subject"])
        self.assertIn(self.user.first_name, context["content_title"])

    def test_get_invitation_context(self):
        self.create_user()
        group = Group(name="My Group", is_private=False)
        roletype = RoleType(name="My Roletype", group_id=group.id)
        invitation = Invitation(
            from_user_id=self.user.id,
            to_user_email="test@example.com",
            with_roletype_id=roletype.id,
            in_group_id=group.id,
        )

        context = self.email_manager.get_invitation_context(
            user=self.user, group=group, roletype=roletype, invitation=invitation
        )

        self._common_test(context=context, template="emails/invitation")

        self.assertEqual(context["email"], invitation.to_user_email)
        self.assertIn("join group", context["subject"])
        self.assertIn(group.name, context["title"])

    def test_get_accepted_invitation_context(self):
        self.create_user()
        user_1 = self.user

        self.create_user()
        group = Group(name="My Group", is_private=False)
        roletype = RoleType(name="My Roletype", group_id=group.id)

        context = self.email_manager.get_accepted_invitation_context(
            user=user_1, group=group, roletype=roletype, host_user=self.user
        )

        self._common_test(context=context, template="emails/invitation")

        self.assertEqual(context["email"], self.user.email)
        self.assertIn("joined group", context["subject"])

    def test_get_cancelled_invitation_context(self):
        self.create_user()
        group = Group(name="My Group", is_private=False)
        roletype = RoleType(name="My Roletype", group_id=group.id)
        invitation = Invitation(
            from_user_id=self.user.id,
            to_user_email="test@example.com",
            with_roletype_id=roletype.id,
            in_group_id=group.id,
        )

        context = self.email_manager.get_cancelled_invitation_context(
            user=self.user, group=group, invitation=invitation
        )

        self._common_test(context=context, template="emails/invitation")

        self.assertEqual(context["email"], invitation.to_user_email)
        self.assertIn("cancelled", context["subject"])
