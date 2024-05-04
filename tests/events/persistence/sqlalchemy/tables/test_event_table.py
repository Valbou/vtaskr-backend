from tests.base_test import BaseTestCase


class TestEventTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "events"
        self.columns_name = [
            "id",
            "created_at",
            "tenant_id",
            "name",
            "data",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
