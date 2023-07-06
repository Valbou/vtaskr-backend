from tests.base_test import BaseTestCase


class TestUserTable(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.table_name = "users"
        self.columns_name = [
            "id",
            "first_name",
            "last_name",
            "email",
            "hash_password",
            "locale",
            "timezone",
            "created_at",
            "last_login_at",
        ]

    def test_table_exists(self):
        self.assertTableExists(self.table_name)

    def test_columns_exists(self):
        self.assertColumnsExists(self.table_name, self.columns_name)
