from unittest import TestCase
from unittest.mock import MagicMock

from src.users.events import UsersEventManager
from src.users.models import (
    Group,
    Invitation,
    RequestChange,
    RequestType,
    RoleType,
    Token,
    User,
)


class TestUsersEventManager(TestCase):
    def setUp(self):
        super().setUp()

        self.manager = UsersEventManager()

    def _create_user(self) -> User:
        return User(first_name="fisrt", last_name="last", email="test@example.com")

    def _create_group(self) -> Group:
        return Group(name="group_123", is_private=False)

    def _create_roletype(self) -> RoleType:
        return RoleType(name="roletype_123")

    def test_send_register_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_register_event(
            session=mock_session,
            user=self._create_user(),
            group=self._create_group(),
        )

        mock_session.emit.assert_called_once()

    def test_send_login_2fa_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        user = self._create_user()
        self.manager.send_login_2fa_event(
            session=mock_session, user=self._create_user(), token=Token(user_id=user.id)
        )

        mock_session.emit.assert_called_once()

    def test_send_email_change_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_email_change_event(
            session=mock_session,
            user=self._create_user(),
            new_email="new_test@example.com",
            request_change=RequestChange(
                request_type=RequestType.EMAIL, email="test@example.com"
            ),
        )

        mock_session.emit.assert_called_once()

    def test_send_password_change_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_password_change_event(
            session=mock_session,
            user=self._create_user(),
            request_change=RequestChange(
                request_type=RequestType.PASSWORD, email="test@example.com"
            ),
        )

        mock_session.emit.assert_called_once()

    def test_send_update_user_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_update_user_event(
            session=mock_session, user=self._create_user()
        )

        mock_session.emit.assert_called_once()

    def test_send_delete_user_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_delete_user_event(
            session=mock_session, user=self._create_user()
        )

        mock_session.emit.assert_called_once()

    def test_send_invitation_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        user = self._create_user()
        group = self._create_group()
        roletype = self._create_roletype()
        invitation = Invitation(
            from_user=user,
            from_user_id=user.id,
            to_user_email="email@exemple.com",
            with_roletype=roletype,
            with_roletype_id=roletype.id,
            in_group=group,
            in_group_id=group.id,
        )

        self.manager.send_invitation_event(
            session=mock_session,
            user=user,
            group=group,
            roletype=roletype,
            invitation=invitation,
        )

        mock_session.emit.assert_called_once()

    def test_send_accepted_invitation_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_accepted_invitation_event(
            session=mock_session,
            to_user=self._create_user(),
            group=self._create_group(),
            roletype=self._create_roletype(),
            from_user=self._create_user(),
        )

        mock_session.emit.assert_called_once()

    def test_send_cancelled_invitation_event(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_cancelled_invitation_event(
            session=mock_session,
            from_user=self._create_user(),
            group=self._create_group(),
        )

        mock_session.emit.assert_called_once()

    def test_send_delete_tenant(self):
        mock_session = MagicMock()
        mock_session.emit = MagicMock()

        self.manager.send_delete_tenant(
            session=mock_session,
            user=self._create_user(),
            members=[self._create_user()],
            group=self._create_group(),
        )

        mock_session.emit.assert_called_once()
