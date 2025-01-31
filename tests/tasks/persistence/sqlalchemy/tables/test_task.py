from tests.base_test import BaseTestCase


class TestTaskTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "tasks"
        self.columns_name = [
            "id",
            "created_at",
            "tenant_id",
            "title",
            "description",
            "emergency",
            "important",
            "scheduled_at",
            "duration",
            "done",
            "assigned_to",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
