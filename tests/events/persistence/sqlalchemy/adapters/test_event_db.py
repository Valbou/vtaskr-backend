from src.events.models import Event
from src.events.persistence.sqlalchemy import EventDB
from tests.base_test import BaseTestCase


class TestEventAdapter(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.event_db = EventDB()
        self.event = Event(
            tenant_id="user_tenant_id",
            name="test:event",
            data={"foo": "bar", "baz": 123},
        )

    def test_crd_event(self):
        with self.app.dependencies.persistence.get_session() as session:
            self.assertIsNone(self.event_db.load(session, self.event.id))
            self.event_db.save(session, self.event)
            session.commit()

        with self.app.dependencies.persistence.get_session() as session:
            event = self.event_db.load(session, self.event.id)
            self.assertDictEqual(event.data, self.event.data)

        with self.app.dependencies.persistence.get_session() as session:
            self.event_db.delete(session, self.event)
            session.commit()
            self.assertFalse(self.event_db.exists(session, self.event.id))
