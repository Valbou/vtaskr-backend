from unittest.mock import MagicMock

from src.events.managers import EventManager
from src.events.models import Event
from tests.base_test import DummyBaseTestCase


class TestEventManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.manager = EventManager(services=self.app.dependencies)

    def test_get_all_tenant_events(self):
        self.manager.services.identity.all_tenants_with_access = MagicMock(
            return_value=["a", "b", "tenant_123", "c"]
        )
        self.manager.event_db.get_all_from_tenant = MagicMock()

        self.manager.get_all_tenant_events(
            session=None, user_id="user_123", tenant_id="tenant_123"
        )

        self.manager.services.identity.all_tenants_with_access.assert_called_once()
        self.manager.event_db.get_all_from_tenant.assert_called_once_with(
            session=None, tenant_id="tenant_123"
        )

    def test_cannot_get_all_tenant_events(self):
        self.manager.services.identity.all_tenants_with_access = MagicMock(
            return_value=[]
        )
        self.manager.event_db.get_all_from_tenant = MagicMock()

        self.manager.get_all_tenant_events(
            session=None, user_id="user_123", tenant_id="tenant_123"
        )

        self.manager.services.identity.all_tenants_with_access.assert_called_once()
        self.manager.event_db.get_all_from_tenant.assert_not_called()

    def test_add(self):
        self.manager.event_db.save = MagicMock()

        event = self.manager.add(
            session=None, tenant_id="tenant_123", event_name="test", data={"foo": "bar"}
        )

        self.manager.event_db.save.assert_called_once()

        self.assertIsInstance(event, Event)
        self.assertDictEqual(event.data, {"foo": "bar"})

    def test_bulk_add(self):
        self.manager.event_db.bulk_save = MagicMock()

        self.manager.bulk_add(session=None, events=[])

        self.manager.event_db.bulk_save.assert_called_once()
