from src.ports import ObserverPort
from tests.base_test import BaseTestCase


EVENT_NAME_TEST = "tests:send:event"


class ObserverTest(ObserverPort):
    event_name = EVENT_NAME_TEST

    @classmethod
    def run(cls, app_ctx, event_name: str, event_data: dict):
        pass


class TestError(Exception):
    pass


class TestEventBus(BaseTestCase):
    def test_0_auto_subscribe(self):
        with self.app.dependencies.eventbus as eventbus_service:
            eventbus_service.set_context(app=self.app)

            self.assertIn(EVENT_NAME_TEST, eventbus_service.index)
            self.assertEqual(len(eventbus_service.index.get(EVENT_NAME_TEST)), 1)
            self.assertEqual(
                eventbus_service.index.get(EVENT_NAME_TEST)[0], ObserverTest.run
            )

    def test_1_manual_subscribe(self):
        def test_function(ctx, event_type, event):
            pass

        with self.app.dependencies.eventbus as eventbus_service:
            self.assertIsNone(eventbus_service.index.get("test"))
            eventbus_service.subscribe(EVENT_NAME_TEST, test_function)
            self.assertEqual(len(eventbus_service.index.get(EVENT_NAME_TEST)), 2)

    def test_2_emit(self):
        def test_raise_function(ctx, event_name, event_data):
            raise TestError(str(event_data))

        with self.assertRaises(TestError) as e:
            with self.app.dependencies.eventbus as eventbus_service:
                eventbus_service.subscribe(EVENT_NAME_TEST, test_raise_function)
                eventbus_service.emit(
                    tenant_id="123",
                    event_name=EVENT_NAME_TEST,
                    event_data={"foo": "bar"},
                )

        self.assertEqual(str(e.exception), ("{'foo': 'bar'}"))
