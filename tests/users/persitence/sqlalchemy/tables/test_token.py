from tests.base_test import BaseTestCase


class TestTokenTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "tokens"
        self.columns_name = [
            "id",
            "created_at",
            "last_activity_at",
            "temp",
            "temp_code",
            "sha_token",
            "user_id",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
