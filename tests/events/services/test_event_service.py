from unittest.mock import MagicMock

from src.events.models import Event
from src.events.services import EventsService
from tests.base_test import DummyBaseTestCase


class TestEventsService(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.event_service = EventsService(services=self.app.dependencies)

    def test_get_all_from_tenant_id(self):
        self.event_service.event_manager.get_all_user_events = MagicMock()

        self.event_service.get_all_user_events(user_id="user_123", tenant_id="abc123")

        self.event_service.event_manager.get_all_user_events.assert_called_once()

    def test_add(self):
        self.event_service.event_manager.add = MagicMock()

        self.event_service.add_event("123abc", event_name="test:service:data", data={})

        self.event_service.event_manager.add.assert_called_once()

    def test_bulk_add(self):
        self.event_service.event_manager.bulk_add = MagicMock()

        events = [
            Event(
                tenant_id="123abc",
                name="test:service:data",
                data={"foo": "bar"},
            )
        ]
        self.event_service.bulk_add_events(events)

        self.event_service.event_manager.bulk_add.assert_called_once()
