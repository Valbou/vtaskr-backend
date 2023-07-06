from tests.base_test import BaseTestCase


class TestTaskTagTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "taskstags"
        self.columns_name = [
            "tag_id",
            "task_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
