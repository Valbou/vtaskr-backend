from unittest.mock import MagicMock, patch

from src.tasks.events import UsersDeleteTenantObserver
from tests.base_test import DummyBaseTestCase

TASKS_SERVICE_PATH = "src.tasks.events.observers.TasksService"


class TestTasksObservers(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.repository_mock = MagicMock()
        self.app.dependencies.persistence.get_repository = MagicMock(
            return_value=self.repository_mock
        )

    def test_users_delete_tenant(self):
        event_data = {
            "targets": ["user_123", "user_456"],
            "from_name": "First Last",
            "tenant_id": "tenant_123",
            "group_id": "group_123",
            "group_name": "Test Group",
        }

        with patch(TASKS_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.clean_all_items_of_tenant = MagicMock()

            UsersDeleteTenantObserver.run(
                self.app, event_name="users:delete:tenant", event_data=event_data
            )

            service.clean_all_items_of_tenant.assert_called_once()

    def test_users_delete_tenant_no_tenant(self):
        event_data = {
            "targets": ["user_123", "user_456"],
            "from_name": "First Last",
            "group_id": "group_123",
            "group_name": "Test Group",
        }

        with patch(TASKS_SERVICE_PATH) as MockClass:
            service = MockClass.return_value
            service.clean_all_items_of_tenant = MagicMock()

            UsersDeleteTenantObserver.run(
                self.app, event_name="users:delete:tenant", event_data=event_data
            )

            service.clean_all_items_of_tenant.assert_not_called()
