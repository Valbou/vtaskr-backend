from unittest.mock import MagicMock, patch

from src.events.services import EventBusService
from tests.base_test import BaseTestCase

EVENT_NAME_TEST = "tests:send:event"


class TestEventBus(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.bus = EventBusService()

    def test_set_context(self):
        ctx = {"app": "app"}

        self.bus.subscribe = MagicMock()

        self.bus.set_context(**ctx)

        self.bus.subscribe.assert_called()
        total = self.bus.subscribe.call_count
        self.assertEqual(total, 7)

    def test_emit(self):
        before = len(self.bus.events)

        self.bus.emit(
            tenant_id="abc123", event_name="event:name", event_data={"foo": "bar"}
        )

        after = len(self.bus.events)
        self.assertEqual(before + 1, after)

    def test_subscribe(self):
        before = len(self.bus.index)

        self.bus.subscribe("event:name", function=str)

        after = len(self.bus.index)
        self.assertEqual(before + 1, after)

    def test_execute(self):
        self.bus.set_context(app=self.app)
        self.bus.emit(
            tenant_id="abc123", event_name="event:name", event_data={"foo": "bar"}
        )

        self.assertEqual(len(self.bus.events), 1)

        with patch("src.events.services.eventbus_service.EventsService") as MockClass:
            service = MockClass.return_value
            service.bulk_add_events = MagicMock()

            self.bus.execute()

            service.bulk_add_events.assert_called_once()

        self.assertEqual(len(self.bus.events), 0)
