from tests.base_test import BaseTestCase


class TestRightTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "rights"
        self.columns_name = [
            "id",
            "created_at",
            "roletype_id",
            "resource",
            "permissions",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
