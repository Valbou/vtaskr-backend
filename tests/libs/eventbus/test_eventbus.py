from src.libs.eventbus import Event
from src.libs.eventbus.register import TestObserver
from tests.base_test import BaseTestCase


class TestError(Exception):
    pass


class TestEventBus(BaseTestCase):
    def test_0_auto_subscribe(self):
        with self.app.eventbus as eventbus_service:
            self.assertIn("tests:send:event", eventbus_service.index)
            self.assertEqual(len(eventbus_service.index.get("tests:send:event")), 1)
            self.assertIsInstance(
                eventbus_service.index.get("tests:send:event")[0], TestObserver
            )

    def test_1_manual_subscribe(self):
        def test_function(ctx, event_type, event):
            pass

        with self.app.eventbus as eventbus_service:
            self.assertIsNone(eventbus_service.index.get("test"))
            eventbus_service.subscribe("test", test_function)
            self.assertEqual(len(eventbus_service.index.get("test")), 1)

    def test_2_emit(self):
        def test_raise_function(ctx, event_type, event):
            raise TestError(str(event))

        event = Event(tenant_id="123", event_type="test", data={"foo": "bar"})

        with self.assertRaises(TestError) as e:
            with self.app.eventbus as eventbus_service:
                eventbus_service.subscribe("test", test_raise_function)
                eventbus_service.emit("test", event)

        self.assertEqual(
            str(e.exception),
            (
                "Event(tenant_id='123', event_type='test', data={'foo': 'bar'},"
                f" created_at='{event.created_at}')"
            ),
        )
