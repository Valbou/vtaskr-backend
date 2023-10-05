from tests.base_test import BaseTestCase


class TestRoleTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "roles"
        self.columns_name = [
            "id",
            "created_at",
            "user_id",
            "group_id",
            "roletype_id",
            "color",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
