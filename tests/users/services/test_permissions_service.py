from tests.base_test import BaseTestCase
from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.users.services import (
    GroupService,
    PermissionControl,
    RightService,
    RoleService,
    RoleTypeService,
)


class CheckCanMixin:
    def check_can(
        self, permission: Permissions, user_id: str, group_id_resource: str
    ) -> bool:
        with self.app.sql.get_session() as session:
            self.permissions_service = PermissionControl(session=session)
            return self.permissions_service.can(
                permission=permission,
                user_id=user_id,
                group_id_resource=group_id_resource,
                resource=Resources.ROLETYPE,
            )


class TestPermissionControl(BaseTestCase, CheckCanMixin):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        self.fake_group_id = self.fake.word()

    def test_user_can_full_use_his_group_as_admin(self):
        self.assertTrue(
            self.check_can(
                permission=Permissions.READ,
                user_id=self.user.id,
                group_id_resource=self.group.id,
            )
        )
        self.assertTrue(
            self.check_can(
                permission=Permissions.ACHIEVE,
                user_id=self.user.id,
                group_id_resource=self.group.id,
            )
        )
        self.assertTrue(
            self.check_can(
                permission=Permissions.CREATE,
                user_id=self.user.id,
                group_id_resource=self.group.id,
            )
        )
        self.assertTrue(
            self.check_can(
                permission=Permissions.UPDATE,
                user_id=self.user.id,
                group_id_resource=self.group.id,
            )
        )
        self.assertTrue(
            self.check_can(
                permission=Permissions.DELETE,
                user_id=self.user.id,
                group_id_resource=self.group.id,
            )
        )

    def test_user_cannot_use_unknown_group(self):
        self.assertFalse(
            self.check_can(
                permission=Permissions.READ,
                user_id=self.user.id,
                group_id_resource=self.fake_group_id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.ACHIEVE,
                user_id=self.user.id,
                group_id_resource=self.fake_group_id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.CREATE,
                user_id=self.user.id,
                group_id_resource=self.fake_group_id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.UPDATE,
                user_id=self.user.id,
                group_id_resource=self.fake_group_id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.DELETE,
                user_id=self.user.id,
                group_id_resource=self.fake_group_id,
            )
        )


class TestPermissionControlOnOthersGroups(BaseTestCase, CheckCanMixin):
    def setUp(self) -> None:
        super().setUp()
        self.create_user()
        first_user = self.user
        self.create_user()

        self.assertNotEqual(first_user.id, self.user.id)

        with self.app.sql.get_session() as session:
            session.expire_on_commit = False

            group_service = GroupService(session)
            self.shared_group = group_service.create_group(
                first_user, "My Shared Group"
            )

            roletype_service = RoleTypeService(session)
            roletype = roletype_service.create_custom_roletype(
                name="Read and Create on RoleType only", group_id=self.shared_group.id
            )

            role_service = RoleService(session)
            role_service.add_role(
                user_id=self.user.id,
                group_id=self.shared_group.id,
                roletype_id=roletype.id,
            )

            right_service = RightService(session)
            right_service.add_right(
                roletype_id=roletype.id,
                resource=Resources.ROLETYPE,
                permissions=[Permissions.READ, Permissions.ACHIEVE],
            )

    # On a group with a custom role (partial access)
    def test_user_can_read_and_achieve_only_on_this_shared_group(self):
        self.assertTrue(
            self.check_can(
                permission=Permissions.READ,
                user_id=self.user.id,
                group_id_resource=self.shared_group.id,
            )
        )
        self.assertTrue(
            self.check_can(
                permission=Permissions.ACHIEVE,
                user_id=self.user.id,
                group_id_resource=self.shared_group.id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.CREATE,
                user_id=self.user.id,
                group_id_resource=self.shared_group.id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.UPDATE,
                user_id=self.user.id,
                group_id_resource=self.shared_group.id,
            )
        )
        self.assertFalse(
            self.check_can(
                permission=Permissions.DELETE,
                user_id=self.user.id,
                group_id_resource=self.shared_group.id,
            )
        )
