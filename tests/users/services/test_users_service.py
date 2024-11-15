from unittest.mock import MagicMock, call

from src.libs.iam.constants import Permissions
from src.settings import LOCALE, TIMEZONE
from src.users.hmi.dto import UserDTO
from src.users.models import (
    Group,
    Invitation,
    RequestChange,
    RequestType,
    Right,
    Role,
    RoleType,
    Token,
    User,
)
from src.users.services import EmailAlreadyUsedError, UsersService
from tests.base_test import DummyBaseTestCase


class TestUsersService(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.users_service = UsersService(services=self.app.dependencies)

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

    def _get_token(self):
        return Token(user_id="user_123")

    def test_create_new_group(self):
        roletype = RoleType(name="Admin", group_id=None)
        group = Group(name="MyGroup", is_private=True)
        role = Role(
            user_id="user_123",
            group_id=group.id,
            roletype_id=roletype.id,
        )

        self.users_service.roletype_manager.get_default_admin = MagicMock(
            return_value=(roletype, False)
        )
        self.users_service.group_manager.create_group = MagicMock(return_value=group)
        self.users_service.right_manager.create_admin_rights = MagicMock()
        self.users_service.role_manager.add_role = MagicMock(return_value=(role, False))
        self.users_service._prepare_observer_roletype = MagicMock()

        new_group = self.users_service.create_new_group(
            user_id="a1", group_name="MyGroup", is_private=True
        )

        self.users_service.roletype_manager.get_default_admin.assert_called_once()
        self.users_service.group_manager.create_group.assert_called_once()
        self.users_service.role_manager.add_role.assert_called_once()

        self.users_service.right_manager.create_admin_rights.assert_not_called()
        self.users_service._prepare_observer_roletype.assert_not_called()

        self.assertEqual(group.id, new_group.id)
        self.assertEqual(group.name, new_group.name)

    def test_get_group(self):
        self.users_service.group_manager.get_group = MagicMock()

        self.users_service.get_group(user_id="user_123", group_id="group_123")

        self.users_service.group_manager.get_group.assert_called_once_with(
            user_id="user_123", group_id="group_123"
        )

    def test_get_update_group(self):
        group = Group(name="Test Group", is_private=False)
        self.users_service.group_manager.update_group = MagicMock()

        self.users_service.update_group(user_id="user_123", group=group)

        self.users_service.group_manager.update_group.assert_called_once()

    def test_get_all_user_groups(self):
        self.users_service.group_manager.get_all_groups = MagicMock()

        self.users_service.get_all_user_groups(user_id="user_123")

        self.users_service.group_manager.get_all_groups.assert_called_once_with(
            user_id="user_123", qs_filters=[]
        )

    def test_get_delete_group(self):
        group = Group(name="Test Group", is_private=False)
        self.users_service.group_manager.delete_group = MagicMock()

        self.users_service.delete_group(user_id="user_123", group=group)

        self.users_service.group_manager.delete_group.assert_called_once()

    def test_get_group_members(self):
        self.users_service.role_manager.get_members = MagicMock()

        self.users_service.get_group_members(user_id="user_123", group_id="group_123")

        self.users_service.role_manager.get_members.assert_called_once_with(
            user_id="user_123", group_id="group_123"
        )

    def test_find_user_by_email(self):
        self.users_service.user_manager.find_user_by_email = MagicMock()

        self.users_service.find_user_by_email(email=self.generate_email())

        self.users_service.user_manager.find_user_by_email.assert_called_once()

    def test_register(self):
        user_dto = UserDTO(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        password = self.generate_password()

        base_user = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            locale=user_dto.locale,
            timezone=user_dto.timezone,
        )
        base_group = Group(name="Private", is_private=True)

        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=False
        )
        self.users_service.user_manager.create_user = MagicMock(return_value=base_user)
        self.users_service.create_new_group = MagicMock(return_value=base_group)
        self.users_service.event_manager.send_register_event = MagicMock()
        self.users_service.email_manager.get_register_context = MagicMock(
            return_value={}
        )
        self.users_service._send_message = MagicMock()

        user, group = self.users_service.register(user_dto, password=password)

        self.users_service.user_manager.find_user_by_email.assert_called_once()
        self.users_service.user_manager.create_user.assert_called_once()
        self.users_service.create_new_group.assert_called_once()
        self.users_service.event_manager.send_register_event.assert_called_once()
        self.users_service.email_manager.get_register_context.assert_called_once()
        self.users_service._send_message.assert_called_once_with(context={})

        self.assertIsInstance(user, User)
        self.assertIsInstance(group, Group)

        self.assertEqual(user.first_name, user_dto.first_name)
        self.assertEqual(user.last_name, user_dto.last_name)
        self.assertEqual(user.email, user_dto.email)
        self.assertEqual(str(user.locale), user_dto.locale)
        self.assertEqual(user.timezone, user_dto.timezone)
        self.assertNotEqual(user.hash_password, password)

        self.assertEqual(group.name, base_group.name)

    def test_clean_unused_accounts(self):
        self.users_service.user_manager.clean_users = MagicMock()

        self.users_service.clean_unused_accounts()

        self.users_service.user_manager.clean_users.assert_called_once()

    def test_authenticate(self):
        base_user = self._get_user()
        base_user.check_password = MagicMock(return_value=True)
        base_user.update_last_login = MagicMock()
        base_token = self._get_token()

        email = (self.generate_email(),)
        password = self.generate_password()

        self.users_service.token_manager.clean_expired = MagicMock()
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )
        self.users_service.token_manager.create_token = MagicMock(
            return_value=base_token
        )
        self.users_service.email_manager.get_login_context = MagicMock(return_value={})
        self.users_service._send_message = MagicMock()

        token = self.users_service.authenticate(email=email, password=password)

        self.users_service.token_manager.clean_expired.assert_called_once()
        self.users_service.user_manager.find_user_by_email.assert_called_once()
        base_user.check_password.assert_called_once()
        base_user.update_last_login.assert_called_once()
        self.users_service.token_manager.create_token.assert_called_once()
        self.users_service.email_manager.get_login_context.assert_called_once_with(
            user=base_user, code=base_token.temp_code
        )
        self.users_service._send_message.assert_called_once_with(context={})

        self.assertIsInstance(token, Token)
        self.assertEqual(base_token.id, token.id)

    def test_authenticate_fail(self):
        base_user = self._get_user()
        base_user.check_password = MagicMock(return_value=False)
        base_user.update_last_login = MagicMock()

        email = (self.generate_email(),)
        password = self.generate_password()

        self.users_service.token_manager.clean_expired = MagicMock()
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )
        self.users_service.token_manager.create_token = MagicMock()
        self.users_service.email_manager.get_login_context = MagicMock()
        self.users_service._send_message = MagicMock()

        token = self.users_service.authenticate(email=email, password=password)

        self.users_service.token_manager.clean_expired.assert_called_once()
        self.users_service.user_manager.find_user_by_email.assert_called_once()
        base_user.check_password.assert_called_once()

        base_user.update_last_login.assert_not_called()
        self.users_service.token_manager.create_token.assert_not_called()
        self.users_service.email_manager.get_login_context.assert_not_called()
        self.users_service._send_message.assert_not_called()

        self.assertIsNone(token)

    def test_get_temp_token(self):
        base_token = self._get_token()
        base_token.is_temp_valid = MagicMock(return_value=True)
        base_token.validate_token = MagicMock(return_value=True)
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.token_manager.update_token = MagicMock()

        token = self.users_service.get_temp_token(
            base_token.sha_token, code=base_token.temp_code
        )

        self.users_service.token_manager.get_token.assert_called_once()
        base_token.is_temp_valid.assert_called_once()
        base_token.validate_token.assert_called_once_with(code=base_token.temp_code)
        self.users_service.token_manager.update_token.assert_called_once()

        self.assertIsInstance(token, Token)
        self.assertEqual(base_token.id, token.id)

    def test_get_expired_temp_token(self):
        base_token = self._get_token()
        base_token.is_temp_valid = MagicMock(return_value=False)
        base_token.validate_token = MagicMock(return_value=True)
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.token_manager.update_token = MagicMock()

        token = self.users_service.get_temp_token(
            base_token.sha_token, code=base_token.temp_code
        )

        self.users_service.token_manager.get_token.assert_called_once()
        base_token.is_temp_valid.assert_called_once()

        base_token.validate_token.assert_not_called()
        self.users_service.token_manager.update_token.assert_not_called()

        self.assertIsNone(token)

    def test_get_token_from_invalid_code(self):
        base_token = self._get_token()
        base_token.is_temp_valid = MagicMock(return_value=True)
        base_token.validate_token = MagicMock(return_value=False)
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.token_manager.update_token = MagicMock()

        token = self.users_service.get_temp_token(
            base_token.sha_token, code=base_token.temp_code
        )

        self.users_service.token_manager.get_token.assert_called_once()
        base_token.is_temp_valid.assert_called_once()
        base_token.validate_token.assert_called_once_with(code=base_token.temp_code)

        self.users_service.token_manager.update_token.assert_not_called()

        self.assertIsNone(token)

    def test_logout(self):
        base_token = self._get_token()

        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.token_manager.delete_token = MagicMock()

        result = self.users_service.logout(sha_token=base_token.sha_token)

        self.users_service.token_manager.get_token.assert_called_once()
        self.users_service.token_manager.delete_token.assert_called_once()

        self.assertTrue(result)

    def test_no_token_logout(self):
        self.users_service.token_manager.get_token = MagicMock(return_value=None)
        self.users_service.token_manager.delete_token = MagicMock()

        result = self.users_service.logout(sha_token="sha_123")  # nosec

        self.users_service.token_manager.get_token.assert_called_once()
        self.users_service.token_manager.delete_token.assert_not_called()

        self.assertFalse(result)

    def test_user_from_token(self):
        base_token = self._get_token()
        base_token.is_valid = MagicMock(return_value=True)
        base_token.update_last_activity = MagicMock()
        base_user = self._get_user()
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.user_manager.get_user = MagicMock(return_value=base_user)

        user = self.users_service.user_from_token(sha_token=base_token.sha_token)

        self.users_service.token_manager.get_token.assert_called_once()
        base_token.is_valid.assert_called_once()
        base_token.update_last_activity.assert_called_once()
        self.users_service.user_manager.get_user.assert_called_once()

        self.assertIsInstance(user, User)
        self.assertEqual(base_user.id, user.id)

    def test_user_from_token_with_temp_token(self):
        base_token = self._get_token()
        base_token.is_valid = MagicMock(return_value=False)
        base_token.update_last_activity = MagicMock()
        base_user = self._get_user()
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.user_manager.get_user = MagicMock(return_value=base_user)

        user = self.users_service.user_from_token(sha_token=base_token.sha_token)

        self.users_service.token_manager.get_token.assert_called_once()
        base_token.is_valid.assert_called_once()
        base_token.update_last_activity.assert_not_called()
        self.users_service.user_manager.get_user.assert_not_called()

        self.assertIsNone(user)

    def test_user_from_token_without_token(self):
        base_token = None
        base_user = self._get_user()
        self.users_service.token_manager.get_token = MagicMock(return_value=base_token)
        self.users_service.user_manager.get_user = MagicMock(return_value=base_user)

        user = self.users_service.user_from_token(sha_token="sha_123")  # nosec

        self.users_service.token_manager.get_token.assert_called_once()
        self.users_service.user_manager.get_user.assert_not_called()

        self.assertIsNone(user)

    def test_request_password_change(self):
        base_user = self._get_user()
        base_request_change = RequestChange(
            request_type=RequestType.PASSWORD, email="test@example.com"
        )
        base_request_change.gen_hash = MagicMock(return_value="hash_123")
        self.users_service.request_change_manager.create_request_change = MagicMock(
            return_value=base_request_change
        )
        self.users_service.email_manager.get_password_change_context = MagicMock(
            return_value={}
        )
        self.users_service._send_message = MagicMock()

        self.users_service.request_password_change(user=base_user)

        self.users_service.request_change_manager.create_request_change.assert_called_once()
        base_request_change.gen_hash.assert_called_once()
        self.users_service.email_manager.get_password_change_context.assert_called_once()
        self.users_service._send_message.assert_called_once_with(context={})

    def test_request_email_change(self):
        user = self._get_user()
        new_email = self.generate_email()
        base_request_change = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )

        self.users_service.request_change_manager.create_request_change = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=None
        )
        self.users_service.email_manager.get_email_change_old_context = MagicMock(
            return_value={"old": True}
        )
        self.users_service.email_manager.get_email_change_new_context = MagicMock(
            return_value={"new": True}
        )
        self.users_service.services.notification.build_message = MagicMock()
        self.users_service.services.notification.add_message = MagicMock()
        self.users_service.services.notification.notify_all = MagicMock()

        self.users_service.request_email_change(user=user, new_email=new_email)

        self.users_service.user_manager.find_user_by_email.assert_called_once()
        self.users_service.request_change_manager.create_request_change.assert_called_once()
        self.users_service.email_manager.get_email_change_old_context.assert_called_once()
        self.users_service.email_manager.get_email_change_new_context.assert_called_once()
        self.users_service.services.notification.build_message.assert_has_calls(
            [call({"old": True}), call({"new": True})]
        )
        self.users_service.services.notification.add_message.assert_called()
        self.users_service.services.notification.notify_all.assert_called_once()

    def test_request_existing_email_change(self):
        user = self._get_user()
        new_email = self.generate_email()
        base_request_change = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )

        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=True
        )
        self.users_service.request_change_manager.create_request_change = MagicMock(
            return_value=base_request_change
        )

        with self.assertRaises(EmailAlreadyUsedError):
            self.users_service.request_email_change(user=user, new_email=new_email)

        self.users_service.user_manager.find_user_by_email.assert_called_once()
        self.users_service.request_change_manager.create_request_change.assert_not_called()

    def test_update_user(self):
        user = self._get_user()

        self.users_service.user_manager.update_user = MagicMock()
        self.users_service.event_manager.send_update_user_event = MagicMock()

        self.users_service.update_user(user)

        self.users_service.user_manager.update_user.assert_called_once()
        self.users_service.event_manager.send_update_user_event.assert_called_once()

    def test_set_new_password(self):
        base_user = self._get_user()
        base_user.set_password = MagicMock()
        password = self.generate_password()
        base_request_change = RequestChange(
            request_type=RequestType.PASSWORD, email="test@example.com"
        )
        base_request_change.check_hash = MagicMock(return_value=True)

        self.users_service.request_change_manager.get_request = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )
        self.users_service.user_manager.update_user = MagicMock()

        result = self.users_service.set_new_password(
            email="test@example.com", hash="hash_123", password=password
        )

        self.users_service.request_change_manager.get_request.assert_called_once()
        base_request_change.check_hash.assert_called_once()
        self.users_service.user_manager.find_user_by_email.assert_called_once()
        base_user.set_password.assert_called_once_with(password=password)
        self.users_service.user_manager.update_user.assert_called_once()

        self.assertTrue(result)

    def test_set_new_password_bad_hash(self):
        password = self.generate_password()
        base_request_change = RequestChange(
            request_type=RequestType.PASSWORD, email="test@example.com"
        )
        base_request_change.check_hash = MagicMock(return_value=False)

        self.users_service.request_change_manager.get_request = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock()

        result = self.users_service.set_new_password(
            email="test@example.com", hash="hash_123", password=password
        )

        self.users_service.request_change_manager.get_request.assert_called_once()
        base_request_change.check_hash.assert_called_once()

        self.users_service.user_manager.find_user_by_email.assert_not_called()

        self.assertFalse(result)

    def test_set_new_email(self):
        base_user = self._get_user()
        base_user.set_email = MagicMock()
        base_request_change = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )
        base_request_change.check_hash = MagicMock(return_value=True)
        base_request_change.check_code = MagicMock(return_value=True)

        self.users_service.request_change_manager.get_request = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )
        self.users_service.user_manager.update_user = MagicMock()
        self.users_service.event_manager.send_update_user_event = MagicMock()

        result = self.users_service.set_new_email(
            old_email="test@example.com",
            new_email="new_test@example.com",
            hash="hash_123",
            code="123",
        )

        self.users_service.request_change_manager.get_request.assert_called_once()
        base_request_change.check_hash.assert_called_once()
        base_request_change.check_code.assert_called_once()
        self.users_service.user_manager.find_user_by_email.assert_called_once()
        base_user.set_email.assert_called_once()
        self.users_service.user_manager.update_user.assert_called_once()
        self.users_service.event_manager.send_update_user_event.assert_called_once()

        self.assertTrue(result)

    def test_set_new_email_bad_hash(self):
        base_user = self._get_user()
        base_request_change = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )
        base_request_change.check_hash = MagicMock(return_value=False)
        base_request_change.check_code = MagicMock(return_value=True)

        self.users_service.request_change_manager.get_request = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )

        result = self.users_service.set_new_email(
            old_email="test@example.com",
            new_email="new_test@example.com",
            hash="hash_123",
            code="123",
        )

        self.users_service.request_change_manager.get_request.assert_called_once()
        base_request_change.check_hash.assert_called_once()

        base_request_change.check_code.assert_not_called()
        self.users_service.user_manager.find_user_by_email.assert_not_called()

        self.assertFalse(result)

    def test_set_new_email_bad_code(self):
        base_user = self._get_user()
        base_request_change = RequestChange(
            request_type=RequestType.EMAIL, email="test@example.com"
        )
        base_request_change.check_hash = MagicMock(return_value=True)
        base_request_change.check_code = MagicMock(return_value=False)

        self.users_service.request_change_manager.get_request = MagicMock(
            return_value=base_request_change
        )
        self.users_service.user_manager.find_user_by_email = MagicMock(
            return_value=base_user
        )

        result = self.users_service.set_new_email(
            old_email="test@example.com",
            new_email="new_test@example.com",
            hash="hash_123",
            code="123",
        )

        self.users_service.request_change_manager.get_request.assert_called_once()
        base_request_change.check_hash.assert_called_once()
        base_request_change.check_code.assert_called_once()

        self.users_service.user_manager.find_user_by_email.assert_not_called()

        self.assertFalse(result)

    def test_delete_admin_user_of_many_groups(self):
        user = self._get_user()
        self.users_service.services.identity.all_tenants_with_access = MagicMock(
            return_value=["123", "456"]
        )
        self.users_service.user_manager.delete_user = MagicMock()

        result = self.users_service.delete_user(user)

        self.users_service.services.identity.all_tenants_with_access.assert_called_once()
        self.users_service.user_manager.delete_user.assert_not_called()

        self.assertFalse(result)

    def test_delete_admin_of_one_or_less_group(self):
        user = self._get_user()
        self.users_service.services.identity.all_tenants_with_access = MagicMock(
            return_value=["123"]
        )
        self.users_service.user_manager.delete_user = MagicMock()
        self.users_service.email_manager.get_delete_context = MagicMock(return_value={})
        self.users_service._send_message = MagicMock()
        self.users_service.event_manager.send_delete_user_event = MagicMock()

        result = self.users_service.delete_user(user)

        self.users_service.services.identity.all_tenants_with_access.assert_called_once()
        self.users_service.user_manager.delete_user.assert_called_once()
        self.users_service.email_manager.get_delete_context.assert_called_once_with(
            user=user
        )
        self.users_service._send_message.assert_called_once()
        self.users_service.event_manager.send_delete_user_event.assert_called_once()

        self.assertTrue(result)

    def test_get_invitations(self):
        self.users_service.invitation_manager.get_from_group = MagicMock(
            return_value=[]
        )

        invitations = self.users_service.get_invitations(
            user_id="user_123", group_id="group_123"
        )

        self.users_service.invitation_manager.get_from_group.assert_called_once()

        self.assertIsInstance(invitations, list)
        self.assertEqual(len(invitations), 0)

    def test_invite_user_by_email(self):
        user = self._get_user()
        base_group = Group(name="Test Group", is_private=False)
        base_roletype = RoleType(name="Test", group_id=base_group.id)

        self.users_service.group_manager.get_group = MagicMock(return_value=base_group)
        self.users_service.roletype_manager.get_roletype = MagicMock(
            return_value=base_roletype
        )
        self.users_service.invitation_manager.update_invitation = MagicMock()
        self.users_service.email_manager.get_invitation_context = MagicMock(
            return_value={}
        )
        self.users_service._send_message = MagicMock()

        invitation = self.users_service.invite_user_by_email(
            user=user,
            user_email="test@example.com",
            group_id=base_group.id,
            roletype_id=base_roletype.id,
        )

        self.users_service.group_manager.get_group.assert_called_once()
        self.users_service.roletype_manager.get_roletype.assert_called_once()
        self.users_service.invitation_manager.update_invitation.assert_called_once()
        self.users_service.email_manager.get_invitation_context.assert_called_once()
        self.users_service._send_message.assert_called_once_with(context={})

        self.assertIsInstance(invitation, Invitation)
        self.assertEqual(invitation.from_user_id, user.id)
        self.assertEqual(invitation.to_user_email, "test@example.com")
        self.assertEqual(invitation.with_roletype_id, base_roletype.id)
        self.assertEqual(invitation.in_group_id, base_group.id)

    def test_accept_invitation(self):
        invited_user = self._get_user()
        base_user = self._get_user()
        base_group = Group(name="Test Group", is_private=False)
        base_roletype = RoleType(name="Testor", group_id=base_group.id)
        base_role = Role(
            user_id=invited_user.id,
            group_id=base_group.id,
            roletype_id=base_roletype.id,
        )
        base_invitation = Invitation(
            from_user_id=base_user.id,
            to_user_email=invited_user.email,
            with_roletype_id=base_roletype.id,
            in_group_id=base_group.id,
        )

        self.users_service.invitation_manager.get_from_hash = MagicMock(
            return_value=base_invitation
        )
        self.users_service.role_manager.add_role = MagicMock(return_value=base_role)
        self.users_service.user_manager.get_user = MagicMock(return_value=base_user)
        self.users_service.group_manager.get_group = MagicMock(return_value=base_group)
        self.users_service.roletype_manager.get_roletype = MagicMock(
            return_value=base_roletype
        )
        self.users_service.email_manager.get_accepted_invitation_context = MagicMock(
            return_value={}
        )
        self.users_service._send_message = MagicMock()
        self.users_service.invitation_manager.delete_invitation = MagicMock()

        role = self.users_service.accept_invitation(user=invited_user, hash="hash_123")

        self.users_service.invitation_manager.get_from_hash.assert_called_once()
        self.users_service.role_manager.add_role.assert_called_once()
        self.users_service.user_manager.get_user.assert_called_once()
        self.users_service.group_manager.get_group.assert_called_once()
        self.users_service.roletype_manager.get_roletype.assert_called_once()
        self.users_service.email_manager.get_accepted_invitation_context.assert_called_once()
        self.users_service._send_message.assert_called_once_with(context={})
        self.users_service.invitation_manager.delete_invitation.assert_called_once()

        self.assertIsInstance(role, Role)
        self.assertEqual(base_role.id, role.id)
        self.assertEqual(base_role.user_id, role.user_id)
        self.assertEqual(base_role.group_id, role.group_id)
        self.assertEqual(base_role.roletype_id, role.roletype_id)

    def test_delete_invitation(self):
        user = self._get_user()
        base_group = Group(name="Test Group", is_private=False)
        base_invitation = Invitation(
            from_user_id="user_123",
            to_user_email="test@example.com",
            with_roletype_id="roletype_id",
            in_group_id="group_123",
        )

        self.users_service.invitation_manager.get_invitation = MagicMock(
            return_value=base_invitation
        )
        self.users_service.group_manager.get_group = MagicMock(return_value=base_group)
        self.users_service.invitation_manager.delete_invitation_by_id = MagicMock(
            return_value=True
        )
        self.users_service.email_manager.get_cancelled_invitation_context = MagicMock()
        self.users_service._send_message = MagicMock()

        self.users_service.delete_invitation(user=user, invitation_id="invitation_123")

        self.users_service.invitation_manager.get_invitation.assert_called_once()
        self.users_service.group_manager.get_group.assert_called_once()
        self.users_service.invitation_manager.delete_invitation_by_id.assert_called_once()
        self.users_service.email_manager.get_cancelled_invitation_context.assert_called_once()
        self.users_service._send_message.assert_called_once()

    def test_cannot_delete_invitation(self):
        user = self._get_user()
        base_group = Group(name="Test Group", is_private=False)
        base_invitation = Invitation(
            from_user_id="user_123",
            to_user_email="test@example.com",
            with_roletype_id="roletype_id",
            in_group_id="group_123",
        )

        self.users_service.invitation_manager.get_invitation = MagicMock(
            return_value=base_invitation
        )
        self.users_service.group_manager.get_group = MagicMock(return_value=base_group)
        self.users_service.invitation_manager.delete_invitation_by_id = MagicMock(
            return_value=False
        )
        self.users_service.email_manager.get_cancelled_invitation_context = MagicMock(
            context={}
        )
        self.users_service._send_message = MagicMock()

        with self.assertRaises(PermissionError):
            self.users_service.delete_invitation(
                user=user, invitation_id="invitation_123"
            )

        self.users_service.invitation_manager.get_invitation.assert_called_once()
        self.users_service.group_manager.get_group.assert_called_once()
        self.users_service.invitation_manager.delete_invitation_by_id.assert_called_once()
        self.users_service.email_manager.get_cancelled_invitation_context.assert_not_called()
        self.users_service._send_message.assert_not_called()

    def test_create_new_right(self):
        base_right = Right(
            roletype_id="roletype_123",
            resource="Test",
            permissions=[Permissions.EXECUTE],
        )

        self.users_service.right_manager.create_right = MagicMock(
            return_value=base_right
        )

        right: Right = self.users_service.create_new_right(
            user_id="user_123", group_id="right_123", right=base_right
        )

        self.assertIsInstance(right, Right)
        self.assertEqual(right.roletype_id, "roletype_123")
        self.assertIs(right.permissions[0], Permissions.EXECUTE)

        self.users_service.right_manager.create_right.assert_called_once()

    def test_get_user_right(self):
        self.users_service.right_manager.get_right = MagicMock(return_value=None)

        result = self.users_service.get_user_right(
            user_id="user_123", right_id="right_123"
        )

        self.assertIsNone(result)

        self.users_service.right_manager.get_right.assert_called_once()

    def test_get_all_user_rights(self):
        self.users_service.right_manager.get_all_rights = MagicMock(return_value=[])

        result = self.users_service.get_all_user_rights(user_id="user_123")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        self.users_service.right_manager.get_all_rights.assert_called_once()

    def test_update_user_right(self):
        self.users_service.right_manager.update_right = MagicMock(return_value=True)

        result = self.users_service.update_user_right(
            user_id="user_id", right=MagicMock(), roletype=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.right_manager.update_right.assert_called_once()

    def test_delete_user_right(self):
        self.users_service.right_manager.delete_right = MagicMock(return_value=True)

        result = self.users_service.right_manager.delete_right(
            user_id="user_123", right=MagicMock(), roletype=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.right_manager.delete_right.assert_called_once()

    def test_create_new_role(self):
        base_role = Role(
            user_id="user_123",
            group_id="group_123",
            roletype_id="roletype_123",
        )

        self.users_service.role_manager.create_role = MagicMock(return_value=base_role)

        role: Role = self.users_service.create_new_role(
            user_id="user_123", role=base_role
        )

        self.assertIsInstance(role, Role)
        self.assertEqual(role.roletype_id, "roletype_123")
        self.assertEqual(role.group_id, "group_123")

        self.users_service.role_manager.create_role.assert_called_once()

    def test_get_user_role(self):
        self.users_service.role_manager.get_role = MagicMock(return_value=None)

        result = self.users_service.get_user_role(
            user_id="user_123", role_id="role_123"
        )

        self.assertIsNone(result)

        self.users_service.role_manager.get_role.assert_called_once()

    def test_get_all_user_roles(self):
        self.users_service.role_manager.get_all_roles = MagicMock(return_value=[])

        result = self.users_service.get_all_user_roles(user_id="user_123")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        self.users_service.role_manager.get_all_roles.assert_called_once()

    def test_update_user_role(self):
        self.users_service.role_manager.update_role = MagicMock(return_value=True)

        result = self.users_service.update_user_role(
            user_id="user_id", role=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.role_manager.update_role.assert_called_once()

    def test_delete_user_role(self):
        self.users_service.role_manager.delete_role = MagicMock(return_value=True)

        result = self.users_service.role_manager.delete_role(
            user_id="user_123", role=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.role_manager.delete_role.assert_called_once()

    def test_create_new_roletype(self):
        base_roletype = RoleType(
            name="Test",
            group_id="group_123",
        )

        self.users_service.roletype_manager.create_custom_roletype = MagicMock(
            return_value=base_roletype
        )

        roletype: RoleType = self.users_service.create_new_roletype(
            name="Test", group_id="group_123"
        )

        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.name, "Test")
        self.assertEqual(roletype.group_id, "group_123")

        self.users_service.roletype_manager.create_custom_roletype.assert_called_once()

    def test_get_user_roletype(self):
        self.users_service.roletype_manager.get_roletype = MagicMock(return_value=None)

        result = self.users_service.get_user_roletype(
            user_id="user_123", roletype_id="roletype_123"
        )

        self.assertIsNone(result)

        self.users_service.roletype_manager.get_roletype.assert_called_once()

    def test_get_all_user_roletypes(self):
        self.users_service.roletype_manager.get_all_roletypes = MagicMock(
            return_value=[]
        )

        result = self.users_service.get_all_user_roletypes(user_id="user_123")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        self.users_service.roletype_manager.get_all_roletypes.assert_called_once()

    def test_update_user_roletype(self):
        self.users_service.roletype_manager.update_roletype = MagicMock(
            return_value=True
        )

        result = self.users_service.update_user_roletype(
            user_id="user_id", roletype=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.roletype_manager.update_roletype.assert_called_once()

    def test_delete_user_roletype(self):
        self.users_service.roletype_manager.delete_roletype = MagicMock(
            return_value=True
        )

        result = self.users_service.roletype_manager.delete_roletype(
            user_id="user_123", roletype=MagicMock()
        )

        self.assertTrue(result)

        self.users_service.roletype_manager.delete_roletype.assert_called_once()
