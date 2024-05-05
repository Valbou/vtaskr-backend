from src.libs.iam.constants import Permissions
from src.users.services import RightService, RoleTypeService, UserService
from tests.base_test import BaseTestCase


class CheckCanMixin:
    def check_can(
        self, permission: Permissions, user_id: str, group_id_resource: str
    ) -> bool:
        with self.app.dependencies.persistence.get_session() as session:
            return self.app.dependencies.identity.can(
                session,
                permission=permission,
                user_id=user_id,
                group_id_resource=group_id_resource,
                resource="RoleType",
                exception=False,
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
                permission=Permissions.EXECUTE,
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
                permission=Permissions.EXECUTE,
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
        first_user, self.first_group = self.user, self.group
        self.create_user()

        self.assertNotEqual(first_user.id, self.user.id)

        user_service = UserService(self.app.dependencies)
        self.shared_group = user_service.create_group(
            user_id=first_user.id, group_name="My Shared Group"
        )

        roletype_service = RoleTypeService(self.app.dependencies)
        roletype = roletype_service.create_custom_roletype(
            name="Read and Create on RoleType only", group_id=self.shared_group.id
        )

        user_service = UserService(self.app.dependencies)
        user_service.add_role(
            user_id=self.user.id,
            group_id=self.shared_group.id,
            roletype_id=roletype.id,
        )

        right_service = RightService(self.app.dependencies)
        right_service.add_right(
            roletype_id=roletype.id,
            resource="RoleType",
            permissions=[Permissions.READ, Permissions.EXECUTE],
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
                permission=Permissions.EXECUTE,
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

    def test_all_tenants_with_read_access_to_group_and_shared(self):
        with self.app.dependencies.persistence.get_session() as session:
            read_roletype_tenant_ids = (
                self.app.dependencies.identity.all_tenants_with_access(
                    session,
                    permission=Permissions.READ,
                    user_id=self.user.id,
                    resource="RoleType",
                )
            )

            self.assertNotIn(self.first_group, read_roletype_tenant_ids)
            self.assertIn(self.group.id, read_roletype_tenant_ids)
            self.assertIn(self.shared_group.id, read_roletype_tenant_ids)

    def test_all_tenants_with_create_access_to_private_group_only(self):
        with self.app.dependencies.persistence.get_session() as session:
            create_roletype_tenant_ids = (
                self.app.dependencies.identity.all_tenants_with_access(
                    session,
                    permission=Permissions.CREATE,
                    user_id=self.user.id,
                    resource="RoleType",
                )
            )

            self.assertNotIn(self.first_group, create_roletype_tenant_ids)
            self.assertIn(self.group.id, create_roletype_tenant_ids)
            self.assertNotIn(self.shared_group.id, create_roletype_tenant_ids)

    def test_all_tenants_with_read_access_on_group_to_private_group_only(self):
        with self.app.dependencies.persistence.get_session() as session:
            create_roletype_tenant_ids = (
                self.app.dependencies.identity.all_tenants_with_access(
                    session,
                    permission=Permissions.READ,
                    user_id=self.user.id,
                    resource="Group",
                )
            )

            self.assertNotIn(self.first_group, create_roletype_tenant_ids)
            self.assertIn(self.group.id, create_roletype_tenant_ids)
            self.assertNotIn(self.shared_group.id, create_roletype_tenant_ids)
