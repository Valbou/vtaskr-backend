from src.events.models import Event
from src.events.services import EventService
from tests.base_test import DummyBaseTestCase


class TestUsersService(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.es = EventService(services=self.app.dependencies)

        self.es.event_db.reset_mock()

    def test_get_all(self):
        self.es.get_all()

        self.es.event_db.get_all.assert_called_once()

    def test_get_all_from_tenant_id(self):
        self.es.get_all_from_tenant_id("abc123")

        self.es.event_db.get_all_from_tenant.assert_called_once()

    def test_add(self):
        self.es.add("123abc", event_name="test:service:data", data={})

        self.es.event_db.save.assert_called_once()

    def test_bulk_add(self):
        events = [
            Event(
                tenant_id="123abc",
                name="test:service:data",
                data={"foo": "bar"},
            )
        ]
        self.es.bulk_add(events)

        self.es.event_db.bulk_save.assert_called_once()
