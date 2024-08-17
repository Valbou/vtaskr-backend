from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
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
from src.users.models import (
    Group,
    Invitation,
    RequestType,
    Right,
    Role,
    RoleType,
    Token,
    User,
)


class EmailAlreadyUsedError(Exception):
    pass


class UsersService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.event = UsersEventService(self.services.eventbus)
        self._define_managers()

    def _send_message(self, context: dict):
        """Helper to send notification message"""

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

        with self.services.persistence.get_session() as session:
            (
                observer_roletype,
                observer_created,
            ) = self.roletype_manager.get_default_observer(session=session)
            session.commit()

            if observer_created:
                self.right_manager.create_observer_rights(
                    session=session, roletype_id=observer_roletype.id
                )

    def create_new_group(
        self, user_id: str, group_name: str, is_private: bool = False
    ) -> Group:
        """
        Create a group and create relation between user and group
        """

        with self.services.persistence.get_session() as session:
            admin_roletype, admin_created = self.roletype_manager.get_default_admin(
                session=session
            )
            session.commit()

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

    def get_group(self, user_id: str, group_id: str) -> Group:
        """Return a user's group"""

        return self.group_manager.get_group(user_id=user_id, group_id=group_id)

    def update_group(self, user_id: str, group: Group) -> bool:
        """Update a user's group"""

        return self.group_manager.update_group(user_id=user_id, group=group)

    def get_all_user_groups(
        self, user_id: str, qs_filters: list[Filter] = []
    ) -> list[Group]:
        """Return a filtered list of user's groups"""

        return self.group_manager.get_all_groups(user_id=user_id, qs_filters=qs_filters)

    def delete_group(self, user_id: str, group: Group) -> bool:
        """Delete a user's group"""

        return self.group_manager.delete_group(user_id=user_id, group=group)

    def get_group_members(self, user_id: str, group_id: str) -> list[Role]:
        """Return all group's members"""

        return self.role_manager.get_members(user_id=user_id, group_id=group_id)

    def find_user_by_email(self, email: str) -> User | None:
        """Find a user from an email"""

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

    def authenticate(self, email: str, password: str) -> Token | None:
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

                return token

        return None

    def get_temp_token(self, sha_token: str, code: str) -> Token | None:
        """Return a temporary token"""

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
        """Invite an user to join a group using his/her email"""

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
        """Permit to a user invited by email to join a group"""

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
        """Remove access to a group"""

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

    def create_new_right(
        self, user_id: str, group_id: str, right: Right
    ) -> Right | None:
        """Create a new right"""

        return self.right_manager.create_right(
            user_id=user_id, group_id=group_id, right=right
        )

    def get_user_right(self, user_id: str, right_id: str) -> Right | None:
        """Return a specific user's right"""

        return self.right_manager.get_right(user_id=user_id, right_id=right_id)

    def get_all_user_rights(
        self, user_id: str, qs_filter: list[Filter] | None = None
    ) -> list[Right]:
        """Return all rights of one user"""

        return self.right_manager.get_all_rights(user_id=user_id, qs_filters=qs_filter)

    def update_user_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Update right associated to user"""

        return self.right_manager.update_right(
            user_id=user_id, right=right, roletype=roletype
        )

    def delete_user_right(self, user_id: str, right: Right, roletype: RoleType) -> bool:
        """Delete a user right"""

        self.right_manager.delete_right(user_id=user_id, right=right, roletype=roletype)

    def create_new_role(self, user_id: str, role: Role) -> Role | None:
        """Create a new role"""

        return self.role_manager.create_role(user_id=user_id, right=role)

    def get_user_role(self, user_id: str, role_id: str) -> Role | None:
        """Return a specific user's role"""

        return self.role_manager.get_role(user_id=user_id, role_id=role_id)

    def get_all_user_roles(
        self, user_id: str, qs_filter: list[Filter] | None = None
    ) -> list[Role]:
        """Return all roles of one user"""

        return self.role_manager.get_all_roles(user_id=user_id, qs_filters=qs_filter)

    def update_user_role(self, user_id: str, role: Role) -> bool:
        """Update role associated to user"""

        return self.role_manager.update_role(user_id=user_id, role=role)

    def delete_user_role(self, user_id: str, role: Role) -> bool:
        """Delete a user role"""

        self.role_manager.delete_role(user_id=user_id, role=role)

    def create_new_roletype(self, name: str, group_id: str) -> RoleType | None:
        """Create a new roletype"""

        return self.roletype_manager.create_custom_roletype(
            name=name, group_id=group_id
        )

    def get_user_roletype(self, user_id: str, roletype_id: str) -> RoleType | None:
        """Return a specific user's roletype"""

        return self.roletype_manager.get_roletype(
            user_id=user_id, roletype_id=roletype_id
        )

    def get_all_user_roletypes(
        self, user_id: str, qs_filter: list[Filter] | None = None
    ) -> list[RoleType]:
        """Return all roletypes of one user"""

        return self.roletype_manager.get_all_roletypes(
            user_id=user_id, qs_filters=qs_filter
        )

    def update_user_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Update roletype associated to user"""

        return self.roletype_manager.update_roletype(user_id=user_id, roletype=roletype)

    def delete_user_roletype(self, user_id: str, roletype: RoleType) -> bool:
        """Delete a user roletype"""

        self.roletype_manager.delete_roletype(user_id=user_id, roletype=roletype)
