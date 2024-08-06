from typing import Tuple

from src.libs.dependencies import DependencyInjector
from src.libs.iam.constants import Permissions
from src.users.events import UsersEventService
from src.users.hmi.dto import UserDTO
from src.users.managers import (
    EmailManager,
    GroupManager,
    InvitationManager,
    RequestChangeManager,
    RightManager,
    RoleManager,
    RoleTypeManager,
    TokenManager,
    UserManager,
)
from src.users.models import Group, Invitation, RequestType, Role, Token, User


class EmailAlreadyUsedError(Exception):
    pass


class UsersService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event = UsersEventService(self.services.eventbus)
        self._define_managers()

    def _send_message(self, context: dict):
        message = self.services.notification.build_message(context)
        self.services.notification.add_message(message=message)
        self.services.notification.notify_all()

    def _define_managers(self):
        """Define managers from domain (no DI here)"""

        self.roletype_manager = RoleTypeManager(services=self.services)
        self.group_manager = GroupManager(services=self.services)
        self.right_manager = RightManager(services=self.services)
        self.role_manager = RoleManager(services=self.services)
        self.request_change_manager = RequestChangeManager(services=self.services)
        self.user_manager = UserManager(services=self.services)
        self.token_manager = TokenManager(services=self.services)
        self.invitation_manager = InvitationManager(services=self.services)
        self.email_manager = EmailManager(services=self.services)

    def _prepare_observer_roletype(self, session):
        """Prepare observer role to add people with minimum rights"""

        (
            observer_roletype,
            observer_created,
        ) = self.roletype_manager.get_default_observer()

        if observer_created:
            self.right_manager.create_observer_rights(session, observer_roletype.id)

    def create_new_group(
        self, user_id: str, group_name: str, is_private: bool = False
    ) -> Group:
        """
        Create a group and create relation between user and group
        """

        admin_roletype, admin_created = self.roletype_manager.get_default_admin()

        with self.services.persistence.get_session() as session:
            group = self.group_manager.create_group(
                session, group_name=group_name, is_private=is_private
            )

            if admin_created:
                self.right_manager.create_admin_rights(session, admin_roletype.id)

            self.role_manager.add_role(
                session,
                user_id=user_id,
                group_id=group.id,
                roletype_id=admin_roletype.id,
            )

            if not is_private:
                self._prepare_observer_roletype(session=session)

        return group

    def find_user_by_email(self, email: str) -> User | None:
        with self.services.persistence.get_session() as session:
            return self.user_manager.find_user_by_email(session, email=email)

    def register(self, user_dto: UserDTO, password: str) -> tuple[User, Group]:
        """Add a new user and his group with admin role"""

        with self.services.persistence.get_session() as session:
            if self.user_manager.find_user_by_email(session, email=user_dto.email):
                raise ValueError(f"User {user_dto.email} already exists")

            user = self.user_manager.create_user(
                session=session,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                email=user_dto.email,
                password=password,
                locale=user_dto.locale,
                timezone=user_dto.timezone,
            )
            session.commit()

        group = self.create_new_group(
            user_id=user.id, group_name="Private", is_private=True
        )

        self.event.send_register_event(user=user, group=group)

        context = self.email_manager.get_register_context(user=user)
        self._send_message(context=context)

        return (user, group)

    def clean_unused_accounts(self):
        """Clean all account whithout last_login_at"""
        self.user_manager.clean_users()

    def authenticate(
        self, email: str, password: str
    ) -> Tuple[Token | None, User | None]:
        """Create a token only if user and password are ok"""

        with self.services.persistence.get_session() as session:
            self.token_manager.clean_expired(session=session)
            session.commit()

            user = self.user_manager.find_user_by_email(session, email)

            if isinstance(user, User) and user.check_password(password):
                # Many tokens can be active for a unique user (it's assumed)
                user.update_last_login()

                token = self.token_manager.create_token(
                    session=session, user_id=user.id
                )
                session.commit()

                context = self.email_manager.get_login_context(
                    user=user, code=token.temp_code
                )
                self._send_message(context=context)

                return token, user

        return None, None

    def get_temp_token(self, sha_token: str, code: str) -> Token | None:
        with self.services.persistence.get_session() as session:
            token = self.token_manager.get_token(session, sha_token=sha_token)

            if (
                code
                and token
                and token.is_temp_valid()
                and token.validate_token(code=code)
            ):
                self.token_manager.update_token(session=session, token=token)
                session.commit()

                return token

        return None

    def logout(self, sha_token: str) -> bool:
        """Delete active token for this user only"""

        with self.services.persistence.get_session() as session:
            token = self.token_manager.get_token(session, sha_token)
            if token:
                self.token_manager.delete_token(session, token)
                session.commit()

                return True

        return False

    def user_from_token(self, sha_token: str) -> User | None:
        """Load a user from a given token"""

        with self.services.persistence.get_session() as session:
            token = self.token_manager.get_token(session, sha_token)

            if token and token.is_valid():
                token.update_last_activity()

                user = self.user_manager.get_user(session, user_id=token.user_id)

                return user

        return None

    def request_password_change(self, user: User) -> None:
        """Create a request to change the user password"""

        request_change = self.request_change_manager.create_request_change(
            user.email, RequestType.PASSWORD
        )
        request_hash = request_change.gen_hash()

        context = self.email_manager.get_password_change_context(
            user=user, sec_hash=request_hash
        )
        self._send_message(context=context)

    def request_email_change(self, user: User, new_email: str) -> None:
        """Generate process to change email"""

        with self.services.persistence.get_session() as session:
            user_found = self.user_manager.find_user_by_email(session, new_email)

        if user_found:
            raise EmailAlreadyUsedError()

        request_change = self.request_change_manager.create_request_change(
            user.email, RequestType.EMAIL
        )

        context_old_email = self.email_manager.get_email_change_old_context(
            user=user,
            request_change=request_change,
        )
        message_old_email = self.services.notification.build_message(context_old_email)
        self.services.notification.add_message(message=message_old_email)

        context_new_email = self.email_manager.get_email_change_new_context(
            user=user, new_email=new_email, sec_hash=request_change.gen_hash()
        )
        message_new_email = self.services.notification.build_message(context_new_email)
        self.services.notification.add_message(message=message_new_email)

        self.services.notification.notify_all()

    def update_user(self, user: User) -> None:
        """Update user"""
        with self.services.persistence.get_session() as session:
            self.user_manager.update_user(session, user)
            session.commit()
            self.event.send_update_user_event(user=user)

    def set_new_password(self, email: str, hash: str, password: str) -> bool:
        """Set the new password to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_manager.get_request(
                session, email, RequestType.PASSWORD
            )

            if request_change and request_change.check_hash(hash=hash):
                user = self.user_manager.find_user_by_email(session, email)
                user.set_password(password=password)
                self.user_manager.update_user(session, user)
                session.commit()

                return True

        return False

    def set_new_email(
        self, old_email: str, new_email: str, hash: str, code: str
    ) -> bool:
        """Set the new email to user if request is ok"""

        with self.services.persistence.get_session() as session:
            request_change = self.request_change_manager.get_request(
                session, old_email, RequestType.EMAIL
            )

            if (
                request_change
                and request_change.check_hash(hash=hash)
                and request_change.check_code(code)
            ):
                user = self.user_manager.find_user_by_email(session, old_email)
                user.set_email(new_email)
                self.user_manager.update_user(session, user)
                session.commit()

                self.event.send_update_user_event(user=user)

                return True

        return False

    def delete_user(self, user: User) -> bool:
        """
        Delete a user if he is not an admin of many groups
        Otherwise it can lead to a deadlock for members left
        """

        with self.services.persistence.get_session() as session:
            group_ids = self.services.identity.all_tenants_with_access(
                session, Permissions.CREATE, user.id, "RoleType"
            )
            if len(group_ids) <= 1:
                self.user_manager.delete_user(session, user)
                session.commit()

                context = self.email_manager.get_delete_context(user=user)
                self._send_message(context=context)

                self.event.send_delete_user_event(user=user)

                return True

        return False

    def get_invitations(self, user_id: str, group_id: str) -> list[Invitation]:
        """Give all invitations associated with group"""

        with self.services.persistence.get_session() as session:
            invitations = self.invitation_manager.get_from_group(
                session=session, user_id=user_id, group_id=group_id
            )

        return invitations

    def invite_user_by_email(
        self, user: User, user_email: str, group_id: str, roletype_id: str
    ) -> Invitation:
        with self.services.persistence.get_session() as session:
            group = self.group_manager.get_group(user_id=user.id, group_id=group_id)
            roletype = self.roletype_manager.get_roletype(
                user_id=user.id, roletype_id=roletype_id
            )

            if group and roletype and not group.is_private:
                invitation = Invitation(
                    from_user_id=user.id,
                    to_user_email=user_email,
                    in_group_id=group.id,
                    with_roletype_id=roletype.id,
                )
                self.invitation_manager.update_invitation(
                    session=session, user_id=user.id, invitation=invitation
                )

                context = self.email_manager.get_invitation_context(
                    user=user, group=group, roletype=roletype, invitation=invitation
                )
                self._send_message(context=context)
            else:
                raise PermissionError()

        return invitation

    def accept_invitation(self, user: User, hash: str) -> Role:
        with self.services.persistence.get_session() as session:
            invitation: Invitation | None = self.invitation_manager.get_from_hash(
                session=session, hash=hash
            )

            if invitation is not None and invitation.to_user_email == user.email:
                role = self.role_manager.add_role(
                    session=session,
                    user_id=user.id,
                    group_id=invitation.in_group_id,
                    roletype_id=invitation.with_roletype_id,
                )

                host_user = self.user_manager.get_user(
                    session=session, id=invitation.from_user_id
                )
                group = self.group_manager.get_group(
                    user_id=user.id, group_id=invitation.in_group_id
                )
                roletype = self.roletype_manager.get_roletype(
                    user_id=invitation.from_user_id,
                    roletype_id=invitation.with_roletype_id,
                )

                context = self.email_manager.get_accepted_invitation_context(
                    user=user, group=group, roletype=roletype, host_user=host_user
                )
                self._send_message(context=context)

                # Delete invitation with another user
                # May lead to permission error if the user lost delete permission
                # The permission will be deleted after expiring delay...
                self.invitation_manager.delete_invitation(
                    session=session,
                    user_id=invitation.from_user_id,
                    invitation=invitation,
                )

                return role

            elif invitation is None:
                raise ValueError("Invitation doesn't exists")
            else:
                raise ValueError("Invitation mismatch user email")

    def delete_invitation(self, user: User, invitation_id: str):
        with self.services.persistence.get_session() as session:
            invitation: Invitation = self.invitation_manager.get_invitation(
                session=session, invitation_id=invitation_id
            )
            group = self.group_manager.get_group(
                user_id=invitation.from_user_id, group_id=invitation.in_group_id
            )

            result = self.invitation_manager.delete_invitation_by_id(
                session=session,
                user_id=user.id,
                group_id=group.id,
                invitation_id=invitation_id,
            )

            if result is False:
                raise PermissionError()
            else:
                context = self.email_manager.get_cancelled_invitation_context(
                    user=user, group=group, invitation=invitation
                )
                self._send_message(context=context)
