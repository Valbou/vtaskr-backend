from datetime import datetime, timedelta
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

from src.settings import LOCALE, TIMEZONE
from src.users.hmi.dto import UserDTO
from src.users.models import Group, RequestChange, RequestType, RoleType, Token, User
from src.users.services import EmailAlreadyUsedError, UserService
from tests.base_test import DummyBaseTestCase


class TestUserService(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.us = UserService(services=self.app.dependencies)

        self.us.user_db.reset_mock()
        self.us.group_db.reset_mock()
        self.us.roletype_db.reset_mock()
        self.us.role_db.reset_mock()
        self.us.right_db.reset_mock()
        self.us.request_change_db.reset_mock()
        self.us.token_db.reset_mock()

        self.us.services.notification.notify_all_calls.clear()
        self.us.services.notification.messages.clear()

    def test_create_admin_rights(self):
        self.us.right_db = MagicMock()
        num_results = self.us._create_admin_rights(roletype_id="132abc")
        self.assertEqual(len(self.us.services.identity.get_resources()), num_results)

    def test_get_default_admin(self):
        new_roletype = RoleType(name="Admin", group_id=None)
        self.us.roletype_db.get_or_create = MagicMock(
            return_value=(new_roletype, False)
        )

        self.us._create_admin_rights = MagicMock()

        roletype = self.us._get_default_admin()

        self.us._create_admin_rights.assert_not_called()

        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.id, new_roletype.id)

    def test_default_admin_created(self):
        new_roletype = RoleType(name="Admin", group_id=None)
        self.us.roletype_db.get_or_create = MagicMock(return_value=(new_roletype, True))

        self.us._create_admin_rights = MagicMock()

        roletype = self.us._get_default_admin()

        self.us._create_admin_rights.assert_called_once()
        self.assertIsInstance(roletype, RoleType)
        self.assertEqual(roletype.id, new_roletype.id)

    def test_request_change(self):
        email = self.generate_email()

        request_change = self.us._request_change(
            email=email, request_type=RequestType.PASSWORD
        )

        self.us.request_change_db.clean_history.assert_called_once()
        self.us.request_change_db.save.assert_called_once()
        self.assertIsInstance(request_change, RequestChange)
        self.assertEqual(request_change.email, email)
        self.assertEqual(request_change.request_type, RequestType.PASSWORD)

    def test_add_role(self):
        self.us.role_db.save = MagicMock()

        role = self.us.add_role(user_id="a1", group_id="b2", roletype_id="c3")

        self.us.role_db.save.assert_called_once()
        self.assertEqual(role.user_id, "a1")
        self.assertEqual(role.group_id, "b2")
        self.assertEqual(role.roletype_id, "c3")

    def test_find_user_by_email(self):
        self.us.find_user_by_email(email=self.generate_email())

        self.us.user_db.find_user_by_email.assert_called_once()

    def test_create_group(self):
        self.us._get_default_admin = MagicMock()
        self.us.add_role = MagicMock()

        group = self.us.create_group(user_id="a1", group_name="MyGroup")

        self.us.group_db.save.assert_called_once()
        self.us._get_default_admin.assert_called_once()
        self.us.add_role.assert_called_once()
        self.assertEqual(group.name, "MyGroup")

    def test_create_private_group(self):
        self.us.create_group = MagicMock()

        self.us.create_private_group(user_id="a1")

        self.us.create_group.assert_called_once()

    def test_register(self):
        user_dto = UserDTO(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        password = self.generate_password()

        self.us.user_db.find_user_by_email.return_value = False
        self.us.roletype_db.get_or_create.return_value = (MagicMock(), MagicMock())
        self.us.event.send_register_event = MagicMock()

        user, group = self.us.register(user_dto, password=password)

        self.us.event.send_register_event.assert_called_once()
        self.assertEqual(len(self.us.services.notification.messages), 1)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 1)

        self.assertIsInstance(user, User)
        self.assertIsInstance(group, Group)

        self.assertEqual(user.first_name, user_dto.first_name)
        self.assertEqual(user.last_name, user_dto.last_name)
        self.assertEqual(user.email, user_dto.email)
        self.assertEqual(str(user.locale), user_dto.locale)
        self.assertEqual(user.timezone, user_dto.timezone)
        self.assertNotEqual(user.hash_password, password)

        self.assertEqual(group.name, "Private")

    def test_clean_unused_accounts(self):
        self.us.clean_unused_accounts()

        self.us.user_db.clean_unused.assert_called_once()

    def test_authenticate_fail(self):
        email = (self.generate_email(),)
        password = self.generate_password()

        token, user = self.us.authenticate(email=email, password=password)

        self.us.token_db.clean_expired.assert_called_once()
        self.us.user_db.find_user_by_email.assert_called_once()
        self.assertIsNone(token)
        self.assertIsNone(user)

    def test_authenticate(self):
        password = self.generate_password()
        email = (self.generate_email(),)
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        user.set_password(password)
        self.us.user_db.find_user_by_email.return_value = user

        token, user = self.us.authenticate(email=email, password=password)

        self.us.token_db.clean_expired.assert_called_once()
        self.us.user_db.find_user_by_email.assert_called_once()
        self.us.token_db.save.assert_called_once()
        self.assertEqual(len(self.us.services.notification.messages), 1)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 1)
        self.assertIsInstance(token, Token)
        self.assertIsInstance(user, User)

    def test_get_temp_token(self):
        created_at = datetime.now(ZoneInfo("UTC")) - timedelta(seconds=90)
        token = Token(  # nosec
            user_id="a1",
            temp=True,
            temp_code="1234",
            sha_token="a1b2c3d4",
            created_at=created_at,
        )
        self.us.token_db.get_token.return_value = token

        up_token = self.us.get_temp_token(
            sha_token=token.sha_token, code=token.temp_code
        )

        self.us.token_db.get_token.assert_called_once()
        self.us.token_db.save.assert_called_once()
        self.assertIsInstance(up_token, Token)
        self.assertEqual(token.id, up_token.id)

    def test_get_expired_temp_token(self):
        created_at = datetime.now(ZoneInfo("UTC")) - timedelta(days=90)
        token = Token(  # nosec
            user_id="a1",
            temp=True,
            temp_code="1234",
            sha_token="a1b2c3d4",
            created_at=created_at,
        )
        self.us.token_db.get_token.return_value = token

        up_token = self.us.get_temp_token(
            sha_token=token.sha_token, code=token.temp_code
        )

        self.us.token_db.get_token.assert_called_once()
        self.us.token_db.save.assert_not_called()
        self.assertIsNone(up_token)

    def test_get_no_temp_token(self):
        self.us.token_db.get_token.return_value = None

        up_token = self.us.get_temp_token(sha_token="a1b2", code="123")  # nosec

        self.us.token_db.save.assert_not_called()
        self.assertIsNone(up_token)

    def test_logout(self):
        token = Token(  # nosec
            user_id="a1",
            temp=False,
            temp_code="1234",
            sha_token="a1b2c3d4",
        )
        self.us.token_db.get_token.return_value = token

        result = self.us.logout(sha_token=token.sha_token)

        self.us.token_db.delete.assert_called_once()
        self.assertTrue(result)

    def test_no_token_logout(self):
        self.us.token_db.get_token.return_value = None

        result = self.us.logout(sha_token="a1b2")  # nosec

        self.us.token_db.delete.assert_not_called()
        self.assertFalse(result)

    def test_user_from_token(self):
        token = Token(  # nosec
            user_id="a1",
            temp=False,
            temp_code="1234",
            sha_token="a1b2c3d4",
        )
        self.us.token_db.get_token.return_value = token

        self.us.user_from_token(sha_token=token.sha_token)

        self.us.user_db.load.assert_called_once()

    def test_user_from_token_with_temp_token(self):
        token = Token(  # nosec
            user_id="a1",
            temp=True,
            temp_code="1234",
            sha_token="a1b2c3d4",
        )
        self.us.token_db.get_token.return_value = token

        self.us.user_from_token(sha_token=token.sha_token)

        self.us.user_db.load.assert_not_called()

    def test_user_from_token_without_token(self):
        self.us.token_db.get_token.return_value = None

        self.us.user_from_token(sha_token="a1b2")  # nosec

        self.us.user_db.load.assert_not_called()

    def test_request_password_change(self):
        email = self.generate_email()
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )

        self.us._request_change = MagicMock(
            return_value=RequestChange(
                request_type=RequestType.PASSWORD,
                email=email,
            )
        )

        self.us.request_password_change(user=user)

        self.us._request_change.assert_called_once()
        self.assertEqual(len(self.us.services.notification.messages), 1)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 1)

    def test_request_email_change(self):
        email = self.generate_email()
        new_email = self.generate_email()
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )

        self.us._request_change = MagicMock(
            return_value=RequestChange(
                request_type=RequestType.EMAIL,
                email=email,
            )
        )
        self.us.user_db.find_user_by_email.return_value = False

        self.us.request_email_change(user=user, new_email=new_email)

        self.us._request_change.assert_called_once()
        self.assertEqual(len(self.us.services.notification.messages), 2)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 1)

    def test_request_existing_email_change(self):
        email = self.generate_email()
        new_email = self.generate_email()
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )

        self.us._request_change = MagicMock(
            return_value=RequestChange(
                request_type=RequestType.EMAIL,
                email=email,
            )
        )
        self.us.user_db.find_user_by_email.return_value = True

        with self.assertRaises(EmailAlreadyUsedError):
            self.us.request_email_change(user=user, new_email=new_email)

        self.us._request_change.assert_called_once()
        self.assertEqual(len(self.us.services.notification.messages), 0)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 0)

    def test_update(self):
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        self.us.event.send_update_user_event = MagicMock()

        self.us.update(user)

        self.us.user_db.update.assert_called_once()
        self.us.event.send_update_user_event.assert_called_once()

    def test_set_new_password(self):
        email = self.generate_email()
        password = self.generate_password()
        new_password = self.generate_password()
        request_change = RequestChange(
            request_type=RequestType.PASSWORD,
            email=email,
        )
        self.us.request_change_db.find_request.return_value = request_change

        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        user.set_password(password)
        self.us.user_db.find_user_by_email.return_value = user

        result = self.us.set_new_password(
            email=email, hash=request_change.gen_hash(), password=new_password
        )

        self.us.user_db.save.assert_called_once()
        self.assertTrue(user.check_password(new_password))
        self.assertTrue(result)

    def test_set_new_password_bad_hash(self):
        email = self.generate_email()
        password = self.generate_password()
        request_change = RequestChange(
            request_type=RequestType.PASSWORD,
            email=email,
        )
        self.us.request_change_db.find_request.return_value = request_change

        result = self.us.set_new_password(email=email, hash="a1b2", password=password)

        self.assertFalse(result)

    def test_set_new_email(self):
        email = self.generate_email()
        new_email = self.generate_email()
        password = self.generate_password()
        request_change = RequestChange(
            request_type=RequestType.EMAIL,
            email=email,
        )
        self.us.request_change_db.find_request.return_value = request_change
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        user.set_password(password)
        self.us.user_db.find_user_by_email.return_value = user
        self.us.event.send_update_user_event = MagicMock()

        result = self.us.set_new_email(
            old_email=email,
            new_email=new_email,
            hash=request_change.gen_hash(),
            code=request_change.code,
        )

        self.us.user_db.save.assert_called_once()
        self.us.event.send_update_user_event.assert_called_once()
        self.assertTrue(result)
        self.assertEqual(user.email, new_email)

    def test_set_new_email_bad_hash(self):
        email = self.generate_email()
        new_email = self.generate_email()
        request_change = RequestChange(
            request_type=RequestType.EMAIL,
            email=email,
        )
        self.us.request_change_db.find_request.return_value = request_change

        result = self.us.set_new_email(
            old_email=email, new_email=new_email, hash="a1b2", code=request_change.code
        )

        self.assertFalse(result)

    def test_set_new_email_bad_code(self):
        email = self.generate_email()
        new_email = self.generate_email()
        request_change = RequestChange(
            request_type=RequestType.EMAIL,
            email=email,
        )
        self.us.request_change_db.find_request.return_value = request_change

        result = self.us.set_new_email(
            old_email=email,
            new_email=new_email,
            hash=request_change.gen_hash(),
            code="1234",
        )

        self.assertFalse(result)

    def test_delete_admin_user_of_many_groups(self):
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        self.us.services.identity.all_tenants_with_access = MagicMock(
            return_value=["123", "456"]
        )

        self.us.delete(user)

        self.assertEqual(len(self.us.services.notification.messages), 0)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 0)
        self.us.user_db.delete.assert_not_called()

    def test_delete_admin_of_one_or_less_group(self):
        user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.generate_email(),
            locale=LOCALE,
            timezone=TIMEZONE,
        )
        self.us.services.identity.all_tenants_with_access = MagicMock(
            return_value=["123"]
        )

        self.us.delete(user)

        self.assertEqual(len(self.us.services.notification.messages), 1)
        self.assertEqual(len(self.us.services.notification.notify_all_calls), 1)
        self.us.user_db.delete.assert_called_once()
