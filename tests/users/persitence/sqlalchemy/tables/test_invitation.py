from tests.base_test import BaseTestCase


class TestInvitationTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "invitations"
        self.columns_name = [
            "id",
            "created_at",
            "from_user_id",
            "to_user_email",
            "with_roletype_id",
            "in_group_id",
            "hash",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
