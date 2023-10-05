from tests.base_test import BaseTestCase


class TestRoleTypeTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "roletypes"
        self.columns_name = [
            "id",
            "created_at",
            "name",
            "group_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
